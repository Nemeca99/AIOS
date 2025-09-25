# Reproducibility One-Pager

Goal: Reproduce a representative CARMA run with measurable artifacts (logs, graphs, indices) in <20 minutes on a local machine.

## Prereqs
- Python 3.11+
- Windows 10/11 (or Linux/macOS)
- Install deps:
```
pip install -r requirements.txt
python -m pip install faiss-cpu graphviz
```

## Step 1: Health + Embeddings + Index
```
python experiments/simple_health_check.py
python experiments/ensure_embeddings.py
```
Artifacts:
- Data/FractalCache/registry.json
- FAISS index built (stdout confirms)

## Step 2: Deep Sleep (Superfragments)
```
python experiments/run_deep_sleep_once.py --force
```
Expected:
- “created N superfrags” in logs
- registry.json count increases

## Step 3: 120-Question Run (Personality + Cognition)
```
python "HiveMind/luna_main.py" --mode real_learning --questions 120
```
Expected:
- Light sleep events present
- Deep sleep may trigger in long runs
- Results saved to AI/personality/learning_results/

## Step 4: Baseline vs CARMA (Optional)
```
python experiments/benchmark_rag_baseline.py --questions 50 --iterations 3
python experiments/benchmark_latency.py --questions 50 --iterations 3
```
Capture:
- Avg latency (baseline vs CARMA)
- Reports in reports/*.csv or stdout

## Step 5: Dependency Graph + Runtime Files
```
python scripts/crawl_dependencies.py --dot dependency_graph.dot --json dependency_report.json
# Render
"C:\Program Files\Graphviz\bin\dot" -Tpng dependency_graph.dot -o dependency_graph.png
"C:\Program Files\Graphviz\bin\dot" -Tsvg dependency_graph.dot -o dependency_graph.svg
```
Artifacts:
- dependency_graph.{dot,png,svg}
- dependency_report.json (runtime file loads)

## Optional: Visual Explorer
```
streamlit run scripts/visualize_dependencies_streamlit.py
```

## Success Criteria (quick)
- FAISS index built
- Deep sleep created superfragments
- 120-Q run completes (100% success)
- Graph + JSON outputs generated

Notes:
- Personality DNA auto-located; ensure file exists at AI_Core/Nova AI/AI/personality/luna_personality_dna.json
- Use --force on deep sleep for small sessions
