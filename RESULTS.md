# Results

**Setup.** Deterministic run (`--execution-mode real --deterministic`), golden suite (n=30: 10 trivial / 10 moderate / 10 high). Every request logs provenance (git_rev, tier, models {main/embedder/SD}, quant, retrieval stats, SD accept/reject, env).

## Routing Accuracy
- Trivial: 100% routed to embedder across all families.
- Moderate/High: ≥ __% correct routing (LLaMA __%, Qwen __%, Phi __%).

## Speculative Decoding
| Arch | Accept Rate (mean) | Accepted Tokens | Rejected Tokens |
|------|---------------------|-----------------|-----------------|
| LLaMA | __% | __ | __ |
| Qwen  | __% | __ | __ |
| Phi   | __% | __ | __ |

## Latency (warm, p95, ms)
| Layer            | LLaMA | Qwen | Phi |
|------------------|------:|-----:|----:|
| Luna + CARMA     |  ___  | ___  | ___ |
| Luna + SimpleRAG |  ___  | ___  | ___ |
| Basic + CARMA    |  ___  | ___  | ___ |

## Retrieval Stability
Median `fragments_found` = __ (IQR __–__) consistent across CARMA and SimpleRAG.

**Mock vs Real.** All results under `execution_mode=real` (watermarked); mock runs excluded from benchmarks.

**Reproducibility.** git_rev=`<hash>`, seed=42, temp=0, golden suite commit=`<hash>`.

---

## Environment Details
- Python: __.__.__
- Platform: __
- CPU: __
- GPU: __
- CUDA: __ (if applicable)

## Provenance Example
```json
{
  "ts":"2025-10-03T17:33:42Z",
  "core":"luna",
  "mode":"interactive", 
  "execution_mode":"real",
  "git_rev":"8ac42e2",
  "env":{"python_version":"3.11.0","platform":"Windows","cpu_model":"Intel Core i7","gpu":"RTX 4090"},
  "models":{"main":"llama-3.2-pkd-deckard-7b-i1","embedder":"llama-3.2-1b-instruct","sd":"mlabonne_qwen3-0.6b"},
  "model_hashes":{"main":"7487b5cc","embedder":"c9e4e46c","sd":"0482783e"},
  "quant":{"main":"Q4_K_M","sd":"Q3_K_L"},
  "router_tier":"moderate",
  "retrieval":{"backend":"carma","k":3,"fragments_found":5},
  "spec_decode":{"accepted":132,"rejected":121,"accept_rate":0.522},
  "cold_warm":"warm",
  "seed":42
}
```
