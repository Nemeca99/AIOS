"""
AIOS Quality Dashboard
Visualizes hypothesis pass rate, latency trends, routing boundary drift, 
A/B buckets, and per-message drilldowns.
"""
from __future__ import annotations
import json
import os
import time
import math
from pathlib import Path
from typing import List, Dict, Any, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
NDJSON_PATH = ROOT / "data_core/analytics/hypotheses.ndjson"
ADAPTIVE_STATE_PATH = ROOT / "data_core/analytics/adaptive_routing_state.json"
GOLDEN_LAST_PATH = ROOT / "data_core/goldens/last_report.json"
GOLDEN_BASELINE_PATH = ROOT / "data_core/goldens/baseline_new.json"

st.set_page_config(page_title="AIOS Quality Dashboard", layout="wide")
st.title("AIOS Quality Dashboard")

@st.cache_data(ttl=10)
def read_ndjson(path: Path) -> List[dict]:
    if not path.exists():
        return []
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                out.append(obj)
            except Exception:
                # skip malformed line
                continue
    return out

@st.cache_data(ttl=10)
def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

@st.cache_data(ttl=10)
def load_frames() -> Tuple[pd.DataFrame, pd.DataFrame]:
    records = read_ndjson(NDJSON_PATH)
    if not records:
        return pd.DataFrame(), pd.DataFrame()
    df = pd.DataFrame(records)

    # Response events (default kind)
    rdf = df[df.get("event_type", "response").fillna("response") == "response"].copy()
    
    # Flatten nested fields safely
    for col in ("meta", "carma", "math_weights", "routing", "adaptive"):
        if col in rdf.columns:
            try:
                expanded = pd.json_normalize(rdf[col].dropna())
                if not expanded.empty:
                    expanded.columns = [f"{col}.{c}" for c in expanded.columns]
                    rdf = pd.concat([rdf.drop(columns=[col], errors='ignore'), expanded], axis=1)
            except:
                pass  # Skip if normalization fails

    # Hypothesis batches
    hdf = df[df.get("event_type") == "hypothesis_batch"].copy()
    # Expand aggregate rates and basic counts
    if not hdf.empty and "results" in hdf.columns:
        hdf["rates.quality"] = hdf["results"].apply(lambda r: (r.get("rates") or {}).get("quality") if isinstance(r, dict) else None)
        hdf["rates.latency"] = hdf["results"].apply(lambda r: (r.get("rates") or {}).get("latency") if isinstance(r, dict) else None)
        hdf["rates.memory"] = hdf["results"].apply(lambda r: (r.get("rates") or {}).get("memory") if isinstance(r, dict) else None)
        hdf["passed"] = hdf["results"].apply(lambda r: r.get("passed") if isinstance(r, dict) else None)
        hdf["failed"] = hdf["results"].apply(lambda r: r.get("failed") if isinstance(r, dict) else None)
        hdf["total"] = hdf["results"].apply(lambda r: r.get("total") if isinstance(r, dict) else None)
        hdf["batch_id"] = hdf["results"].apply(lambda r: r.get("batch_id") if isinstance(r, dict) else None)
    return rdf, hdf

@st.cache_data(ttl=10)
def load_adaptive_state() -> dict:
    return read_json(ADAPTIVE_STATE_PATH)

@st.cache_data(ttl=10)
def load_golden() -> Tuple[dict, dict]:
    return read_json(GOLDEN_LAST_PATH), read_json(GOLDEN_BASELINE_PATH)

rdf, hdf = load_frames()
adaptive_state = load_adaptive_state()
last_report, baseline = load_golden()

# Sidebar filters
st.sidebar.header("Filters")
conv_ids = sorted([c for c in rdf.get("conv_id", pd.Series(dtype=str)).dropna().unique().tolist()]) if not rdf.empty else []
conv_sel = st.sidebar.multiselect("Conversation IDs", conv_ids, default=conv_ids[:5] if len(conv_ids) > 0 else [])
window = st.sidebar.selectbox("Aggregation window", ["None", "1m", "5m", "15m", "1h"], index=2)

# Auto-refresh
if st.sidebar.checkbox("Auto-refresh (10s)", value=False):
    time.sleep(10)
    st.rerun()

# Top summary
col1, col2, col3, col4 = st.columns(4)

# Hypothesis pass rate
if not hdf.empty and "total" in hdf.columns and "passed" in hdf.columns:
    total_cases = int(hdf["total"].dropna().sum())
    total_pass = int(hdf["passed"].dropna().sum())
    pass_rate = (total_pass / total_cases) if total_cases > 0 else None
else:
    total_cases = total_pass = pass_rate = None

# Routing metrics from adaptive state
control_count = adaptive_state.get("buckets", {}).get("control", {}).get("sample_count", 0)
treatment_count = adaptive_state.get("buckets", {}).get("treatment", {}).get("sample_count", 0)
treatment_boundary = adaptive_state.get("buckets", {}).get("treatment", {}).get("boundary", 0.5)

col1.metric("Hypothesis pass rate", f"{pass_rate:.0%}" if pass_rate is not None else "n/a", 
            help="Percentage of hypothesis tests that passed")
col2.metric("Control samples", f"{control_count}", help="Messages processed in control bucket")
col3.metric("Treatment samples", f"{treatment_count}", help="Messages processed in treatment bucket")
col4.metric("Treatment boundary", f"{treatment_boundary:.3f}", 
            delta=f"{treatment_boundary - 0.5:+.3f}" if treatment_boundary != 0.5 else None,
            help="Current routing boundary for treatment bucket")

st.divider()

# Tabs
T1, T2, T3, T4, T5 = st.tabs([
    "Overview", "Hypotheses", "Routing", "Drill-down", "Settings"
])

with T1:
    st.subheader("Traffic split and sources")
    if rdf.empty:
        st.info("No response events yet. Run some questions through Luna to see data.")
    else:
        dfv = rdf.copy()
        if conv_sel:
            dfv = dfv[dfv["conv_id"].isin(conv_sel)]
        
        # Traffic by source (main_model vs embedder)
        source_col = "meta.source" if "meta.source" in dfv.columns else None
        
        c1, c2 = st.columns(2)
        
        # Bucket distribution
        if adaptive_state.get("total_conversations", 0) > 0:
            bucket_data = pd.DataFrame([
                {"bucket": "control", "count": control_count},
                {"bucket": "treatment", "count": treatment_count}
            ])
            c1.plotly_chart(px.pie(bucket_data, names="bucket", values="count", 
                                  title="A/B Bucket Distribution"), 
                          use_container_width=True)
        else:
            c1.info("No A/B bucket data yet")
        
        # Source distribution
        if source_col and source_col in dfv.columns:
            vs = dfv[source_col].fillna("unknown").value_counts().reset_index()
            vs.columns = ["source", "count"]
            c2.plotly_chart(px.pie(vs, names="source", values="count", 
                                  title="Routing Source (main_model vs embedder)"), 
                          use_container_width=True)
        else:
            c2.info("No routing source data in logs yet")

with T2:
    st.subheader("Hypothesis batches")
    if hdf.empty:
        st.info("No hypothesis batches logged yet. Hypothesis tests run periodically after messages accumulate.")
    else:
        # Basic table
        cols = ["ts", "conv_id", "msg_id", "passed", "failed", "rates.quality", "rates.latency", "rates.memory", "batch_id"]
        view = hdf[[c for c in cols if c in hdf.columns]].sort_values("ts", ascending=False)
        st.dataframe(view, use_container_width=True, height=300)
        
        # Trend: quality fail rate over time
        if "rates.quality" in hdf.columns:
            ht = hdf.dropna(subset=["rates.quality"]).copy()
            if not ht.empty:
                ht["timestamp"] = pd.to_datetime(ht.get("ts", pd.Timestamp.utcnow()))
                st.plotly_chart(
                    px.line(ht, x="timestamp", y="rates.quality", markers=True, 
                           title="Quality fail rate over time"),
                    use_container_width=True
                )

with T3:
    st.subheader("Boundary drift and adaptive signals")
    if rdf.empty:
        st.info("No response events yet.")
    else:
        dfv = rdf.copy()
        if conv_sel:
            dfv = dfv[dfv["conv_id"].isin(conv_sel)]
        
        # Extract boundary and weight
        boundary_col = "math_weights.adaptive.boundary" if "math_weights.adaptive.boundary" in dfv.columns else None
        weight_col = "math_weights.calculated_weight" if "math_weights.calculated_weight" in dfv.columns else None
        time_col = "ts" if "ts" in dfv.columns else None
        
        if boundary_col and time_col:
            dfb = dfv.dropna(subset=[boundary_col]).copy()
            if not dfb.empty:
                dfb["timestamp"] = pd.to_datetime(dfb[time_col])
                st.plotly_chart(
                    px.line(dfb, x="timestamp", y=boundary_col, 
                           title="Effective routing boundary over time"),
                    use_container_width=True
                )
            else:
                st.info("No boundary data in logs yet (adaptive routing may not have adjusted yet)")
        
        if weight_col and time_col:
            dfw = dfv.dropna(subset=[weight_col]).copy()
            if not dfw.empty:
                dfw["timestamp"] = pd.to_datetime(dfw[time_col])
                st.plotly_chart(
                    px.scatter(dfw, x="timestamp", y=weight_col, 
                             title="Calculated conversation weight over time", opacity=0.6),
                    use_container_width=True
                )
        
        # Notes from adaptive
        if "math_weights.adaptive.adaptive_metadata" in dfv.columns:
            notes_df = dfv.dropna(subset=["math_weights.adaptive.adaptive_metadata"])
            if not notes_df.empty:
                st.write("Recent adaptive adjustments:")
                st.dataframe(
                    notes_df[["ts", "conv_id", "math_weights.adaptive.adaptive_metadata"]].tail(10),
                    use_container_width=True,
                    height=220
                )

with T4:
    st.subheader("Per-message events")
    if rdf.empty:
        st.info("No response events yet.")
    else:
        # Show available columns
        cols = [c for c in [
            "ts", "conv_id", "msg_id", "question", "trait", "meta.source",
            "math_weights.adaptive.bucket", "math_weights.adaptive.boundary",
            "math_weights.calculated_weight", "math_weights.mode",
            "carma.fragments_found"
        ] if c in rdf.columns]
        
        if cols:
            view = rdf[cols].sort_values("ts", ascending=False) if "ts" in rdf.columns else rdf[cols]
            st.dataframe(view, use_container_width=True, height=450)
        else:
            st.warning("Response events found but no recognized columns. Check log format.")

with T5:
    st.subheader("Settings and diagnostics")
    st.write("**Paths:**")
    st.code(str(NDJSON_PATH))
    st.code(str(ADAPTIVE_STATE_PATH))
    st.code(str(GOLDEN_LAST_PATH))
    st.code(str(GOLDEN_BASELINE_PATH))
    
    st.write("**Adaptive state (raw):**")
    st.json(adaptive_state or {})
    
    st.write("**Files status:**")
    st.write(f"- NDJSON events: {len(rdf)} response events, {len(hdf)} hypothesis batches")
    st.write(f"- Adaptive conversations tracked: {adaptive_state.get('total_conversations', 0)}")
    st.write(f"- Control bucket samples: {control_count}")
    st.write(f"- Treatment bucket samples: {treatment_count}")

st.caption("Updates every ~10s with auto-refresh enabled. Adjust cache TTLs in code if needed.")

