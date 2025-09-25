import sys
import os
import unittest

# Ensure the UML_Calculator_V1 directory is in sys.path for absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Discover and run all test files in the UML_Calculator_V1 directory and subdirectories
if __name__ == "__main__":
    loader = unittest.TestLoader()
    # Discover all test_*.py and *_test.py files, including operation module tests
    suite = loader.discover(start_dir=current_dir, pattern="test_*.py")
    # Also include uml_test_suite.py if it doesn't match the pattern
    suite2 = loader.discover(start_dir=current_dir, pattern="uml_test_suite.py")
    all_tests = unittest.TestSuite([suite, suite2])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(all_tests)
    sys.exit(not result.wasSuccessful())
