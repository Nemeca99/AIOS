"""
Division operation for UML Calculator
Supports context-aware and advanced logic, including recursive zero identity.
"""


def divide(a, b, context=None, verbose=False):
    # Recursive zero identity logic
    if a == 0 and b == 0:
        result = 1.0  # Recursive unity
    elif a == 0 and b == -0:
        result = 1.0  # Recursive zero identity
    elif a == -0 and b == 0:
        result = -1.0  # Mirror identity
    elif a == -0 and b == -0:
        result = 1.0  # Recursive unity
    elif b == 0:
        result = a  # Positive zero identity
    elif b == -0:
        result = -a  # Negative zero inversion
    else:
        result = a / b
    if verbose:
        print(f"divide({a}, {b}) = {result}")
    return result
