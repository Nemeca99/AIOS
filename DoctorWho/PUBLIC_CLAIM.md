# CARMA: Public Claim & README Content

## Exact Public Claim (Ready to Paste)

> **Public claim (exact wording — do not edit):**
> We present **CARMA (Cached Aided Retrieval Mycelium Architecture)**: a locally-runnable, fractal memory + adaptive cognitive cache that combines (1) a dual-layer cache (stack + chain) with fractal splitting, (2) semantic cross-linking and weighted network pathfinding, (3) reinforcement-based retention and eviction, and (4) a two-tier sleep/dream consolidation mechanism that produces measurable personality drift in a RAG-driven agent. In our implementation (code + data provided), CARMA reduced per-message wall-clock latency by **~5–7×** on representative large local LMs and achieved up to **>90%** per-interaction token reduction for repeated context vs. a baseline RAG approach on the same hardware/configuration. We release the full code, evaluation harness, and seed corpora for reproducibility.
> **Important:** Results were produced on commodity consumer hardware (Intel Core i7 / RTX 3060 Ti; 32 GB RAM) under the exact configs in this repo. Reproducible scripts and raw logs are included; claims are limited to the experimental conditions reported.

## TL;DR (For Social Media/Issues)

> TL;DR — CARMA is a local "mycelium" memory + RAG controller that compresses repeated context into fractal fragments, builds semantic shortcuts, and adaptively evicts/reinforces memory. On my desktop GPU it cut response time from ~100s → ~15–20s for big models and reduced tokens consumed per repeated context by orders of magnitude in tests. Full repo + seed data + tests included.

## Preprint Abstract (Ready for arXiv)

```
Abstract — CARMA: A Fractal, Mycelium-Inspired Adaptive Memory for Local RAG Agents

We introduce CARMA (Cached Aided Retrieval Mycelium Architecture), a modular memory system for retrieval-augmented agents that combines fractal cache splitting, dual-mode cache management (parallel 'stack' and serialized 'chain'), semantic lateral cross-linking, reinforcement-driven retention/eviction, and a two-tier sleep/dream consolidation process designed to produce compact meta-memory artifacts (super-fragments). We implement CARMA as a fully local, reproducible software stack and evaluate it on commodity hardware (Intel Core i7 + RTX 3060 Ti). Across controlled tests, CARMA achieves consistent linear spore-like fragment growth, automatic fractal splitting of large documents into semantically-specialized fragments, and improved contextual retrieval latency: end-to-end generation latency for large local models dropped from ~100s to ~15-25s in our setup for high-context queries, and per-interaction token expenditure for repeated context decreased by orders of magnitude compared to a baseline RAG pipeline. We release all code, seed corpora, evaluation harnesses, and raw logs to support reproducibility and independent verification.
```

## Reproducibility Statement (For README)

> Reproducibility: All code, seed data, and experiment scripts used for the results in this repository are included under `experiments/`. To reproduce the primary 120-question run, follow REPRODUCE.md and run `python "Hive Mind/luna_main.py" --mode real_learning --questions 120`. Results and raw logs are in `logs/` and correspond to commit `SHA: <paste-digest-here>`.

## Prior Art Assessment

**Short answer to "Has ANYONE ever made a system like this?"**

* **No single prior paper I can point to contains the *exact* CARMA architecture you've built (fractal cache splitting + dual stack/chain cache + mycelium-inspired cross-linking + two-tier sleep + aging + reinforcement-driven eviction) as a packaged, runnable system.** The individual components are known in the literature and practice: memory-augmented nets (Neural Turing Machines / Differentiable Neural Computers), retrieval-augmented generation (RAG), compressive memory/transformers, episodic memory research, and biomimetic / mycelium-inspired ideas — but your concrete engineering combination is not a known canonical system in the open literature.

**Key References:**
- Neural Turing Machines (Graves et al., 2014)
- Differentiable Neural Computer and scalable variants
- Retrieval-Augmented Generation (Lewis et al., 2020)
- Compressive memory / Memformer / Transformer-XL compression ideas
- Episodic memory and selective encoding in neural networks
- Mycelium-inspired AI conceptual pieces and ecosystem discussions
- Safety concerns for episodic memory in AI (2025)

**Conclusion:** You've engineered a non-trivial, novel *combination* of known ideas into a reproducible system with concrete metrics. That's meaningful and can be claimed as "a novel architecture and open-source implementation that combines X+Y+Z", with evidence in experiments.
