# Blackwall Lexicon & Fragment System

This document details the dual-hemisphere lexicon architecture, emotional weight mapping, synonym normalization, and integration with the fragment system. See SYSTEMS_SUMMARY.md for a high-level overview.

## Dual Hemisphere Architecture
- **Left Hemisphere:** Maps words to emotional fragment weights (Desire, Logic, Compassion, Stability, Autonomy, Recursion, Protection, Vulnerability, Paradox)
- **Right Hemisphere:** Maps word variants and synonyms to canonical root words for normalization

## Integration
- Tokenize input → Normalize (right) → Weight (left) → Dynamic fusion
- Fragment weights are dynamic and context-sensitive

## Example JSON Structure
- Left: `{ "love": { "Desire": 60.0, "Compassion": 40.0 } }`
- Right: `{ "loving": "love" }`

## See Also
- SYSTEMS_SUMMARY.md (fragment table)
- fragment_profiles_and_blends.json (fragment definitions)
