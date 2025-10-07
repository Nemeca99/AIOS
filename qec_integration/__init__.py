"""
QEC → AIOS Integration Package

Borrows battle-tested code from Quantum Entanglement Chess (QEC) project
to enhance AIOS with:
- Invariant budget system (quality control)
- Performance benchmarks (regression detection)
- Schema validation (data integrity)
- Hypothesis testing (research validation)

Author: Travis Miner
"""

__version__ = "1.0.0"
__author__ = "Travis Miner"

# Import key components
try:
    from .aios_invariant_budget import QECInvariantBudget as AIOSInvariantBudget
    from .aios_performance_benchmarks import QECPerformanceBenchmark as AIOSPerformanceBenchmark
    from .aios_schema_validator import QECSchemaValidator as AIOSSchemaValidator
    from .aios_hypothesis_tester import QECHypothesisTester as AIOSHypothesisTester
    
    __all__ = [
        'AIOSInvariantBudget',
        'AIOSPerformanceBenchmark',
        'AIOSSchemaValidator',
        'AIOSHypothesisTester'
    ]
    
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ QEC Integration not fully available: {e}")
    INTEGRATION_AVAILABLE = False
    __all__ = []

# Integration status
print(f"🎯 QEC → AIOS Integration v{__version__}")
if INTEGRATION_AVAILABLE:
    print("   ✅ All components loaded successfully")
else:
    print("   ⚠️ Some components unavailable")

