# directives_registry.py
# Imports and initializes all active core directives

from directive_003_recursive_trust import RecursiveTrustProtocol
from margin_of_signal import MarginOfSignal

def initialize_directives():
    trust = RecursiveTrustProtocol()
    margin = MarginOfSignal()
    print("✅ Core directives initialized.")
    return {
        "trust_protocol": trust,
        "margin_of_signal": margin
    }
