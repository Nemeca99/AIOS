# This script will be used to compute and tag per-memory fragment weights for each memory chunk.
# It will be imported and used in summarize_and_index_memories.py

import json
import os
from core.blackwall_pipeline import BlackwallPipeline

# Path to fragment weights and lexicon/thesaurus (update as needed)
FRAGMENT_WEIGHTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'personality', 'fragment_weights.json')
LEFT_LEXICON_PATH = os.path.join(os.path.dirname(__file__), 'core', 'left_master.json')
RIGHT_THESAURUS_PATH = os.path.join(os.path.dirname(__file__), 'core', 'right_master.json')

# Load fragment weights
with open(FRAGMENT_WEIGHTS_PATH, 'r', encoding='utf-8') as f:
    fragment_weights = json.load(f)

# Load Blackwall pipeline
pipeline = BlackwallPipeline(
    left_master_path=LEFT_LEXICON_PATH,
    right_master_path=RIGHT_THESAURUS_PATH,
    fragments=fragment_weights
)

def compute_fragment_weights_for_text(text):
    """
    For a given text, compute the weights for each fragment/personality.
    Returns: {fragment: {trait: value, ...}, ...}
    """
    roots = pipeline.filter_and_map(text)
    print(f"[DEBUG] Roots for text: {roots}")
    weights = {}
    for fragment in fragment_weights:
        weights[fragment] = pipeline.get_weighted_profile(roots)
        print(f"[DEBUG] Weights for fragment {fragment}: {weights[fragment]}")
    return weights
