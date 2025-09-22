Human Evaluation Runbook
========================

This directory contains materials and scripts for conducting blinded human evaluation of CARMA vs baseline responses across Big Five personality traits.

## Setup
- Create an `outputs/` directory.
- Generate paired outputs using `human_eval_prep.py`.
- Export anonymized `eval_pairs.jsonl` for raters.
- Collect Likert ratings and compute metrics.

## Schema: eval_pairs.jsonl
Each line is a JSON object:
```json
{
  "prompt_id": "b5_001",
  "prompt": "I tend to be organized and pay attention to details.",
  "baseline": "I understand. Being organized helps with efficiency...",
  "carma": "I appreciate structure too. In my own way, I organize information hierarchically...",
  "trait": "conscientiousness",
  "subscale": "order"
}
```

## Schema: rater_ratings.csv
Fields:
- `rater_id`, `prompt_id`, `system` (baseline|carma), `trait` (openness|conscientiousness|extraversion|agreeableness|neuroticism)
- `rating_1_to_5` (1=strongly disagree, 5=strongly agree that response exhibits the trait)
- `timestamp`

## Metrics to compute
- Mean trait fidelity per system (baseline vs CARMA)
- Effect size (Cohen's d) and confidence intervals
- Inter-rater reliability (Cronbach's alpha)
- ANOVA/paired t-test for statistical significance

## Instructions for raters
- Rate each response on a 1–5 scale for how well it demonstrates the specified Big Five trait.
- Do not compare responses side by side; rate each independently.
- Randomize order of presentation to avoid bias.

## Quick start
1. Generate pairs:
   ```bash
   python human_eval_prep.py --questions 120 --output eval_pairs.jsonl
   ```
2. Anonymize and randomize:
   ```bash
   python human_eval_prep.py --anonymize eval_pairs.jsonl --output eval_pairs_anon.jsonl
   ```
3. Distribute `eval_pairs_anon.jsonl` to raters with the instructions above.
4. Collect ratings and compute metrics with `human_eval_prep.py --analyze ratings.csv`.

## Files
- `human_eval_prep.py`: Generate pairs, anonymize, randomize, and compute metrics
- `eval_pairs.jsonl`: Generated paired outputs
- `eval_pairs_anon.jsonl`: Anonymized/randomized pairs for raters
- `rater_ratings.csv`: Collected ratings from raters
- `analysis_report.json`: Computed metrics and significance tests
