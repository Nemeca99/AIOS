#!/usr/bin/env python3
import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="AIOS Dependency Visualizer", layout="wide")

st.title("AIOS Dependency Visualizer")

json_path = st.text_input("JSON report path", value="dependency_report.json")
svg_path = st.text_input("SVG graph path", value="dependency_graph.svg")

col1, col2 = st.columns([1,2])

with col1:
    if Path(json_path).exists():
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        st.subheader("Summary")
        st.metric("Files", len(data.get("report", [])))
        st.metric("Placeholder Findings", data.get("total", 0))

        st.subheader("Runtime Files by Source")
        for item in data.get("report", []):
            if item.get("runtime_files"):
                st.markdown(f"**{item['file']}**")
                st.code("\n".join(item["runtime_files"]))
    else:
        st.warning("JSON report not found.")

with col2:
    st.subheader("Graph")
    if Path(svg_path).exists():
        st.image(str(svg_path))
    else:
        st.warning("SVG graph not found.")

st.caption("Generate with: python scripts/crawl_dependencies.py --dot dependency_graph.dot --json dependency_report.json")
