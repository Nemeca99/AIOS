"""
CLI interface for the UML Calculator
"""

import argparse
from core.uml_core import parse_uml, eval_uml
from core.converters import convert_standard_to_uml
from utils.safe_eval import safe_eval

# Colorama import for colored output (optional)
try:
    import colorama

    colorama.init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False


def color_text(text, color):
    if not COLOR_ENABLED:
        return text
    codes = {
        "prompt": "\033[96m",  # Cyan
        "result": "\033[92m",  # Green
        "error": "\033[91m",  # Red
        "info": "\033[93m",  # Yellow
        "reset": "\033[0m",
    }
    return f"{codes.get(color, '')}{text}{codes['reset']}"


def print_result(expr, result, mode=None, extra_info=None):
    """Print calculation result with consistent formatting"""
    if mode:
        print(f"[{mode}] ", end="")
    print(f"{expr} = {result}", end="")
    if extra_info:
        print(f" ({extra_info})")
    else:
        print()


def evaluate_expression(expr, mode="auto", show_steps=False):
    """
    Evaluate an expression using the UML calculator
    Args:
        expr: Expression to evaluate
        mode: Calculation mode (auto, standard, uml, ris)
        show_steps: Whether to show calculation steps
    Returns:
        tuple: (result, steps)
    """
    steps = []
    result = None
    if show_steps:
        steps.append(f"Original expression: {expr}")
    # Auto mode tries different approaches
    if mode == "auto" or mode == "standard":
        try:
            result = safe_eval(expr)
            if show_steps:
                steps.append(f"Standard evaluation: {result}")
            if mode == "standard":
                return result, steps
        except Exception as e:
            if show_steps:
                steps.append(f"Standard evaluation failed: {str(e)}")
    if mode == "auto" or mode == "uml":
        try:
            parsed = parse_uml(expr)
            if show_steps:
                steps.append(f"UML parsing: {parsed}")
            result = eval_uml(parsed)
            if show_steps:
                steps.append(f"UML evaluation: {result}")
            return result, steps
        except Exception as e:
            if show_steps:
                steps.append(f"Direct UML parsing failed: {str(e)}")
            try:
                uml_expr = convert_standard_to_uml(expr)
                if show_steps:
                    steps.append(f"Converted to UML: {uml_expr}")
                parsed = parse_uml(uml_expr)
                result = eval_uml(parsed)
                if show_steps:
                    steps.append(f"UML evaluation: {result}")
                return result, steps
            except Exception as e2:
                if show_steps:
                    steps.append(f"Conversion to UML failed: {str(e2)}")
    if mode == "ris":
        try:
            a, b = map(float, expr.split(","))
            from core.ris import ris

            result = ris(a, b)
            if show_steps:
                steps.append(f"RIS evaluation: {result}")
            return result, steps
        except Exception as e:
            if show_steps:
                steps.append(f"RIS evaluation failed: {str(e)}")
    return result, steps


def main():
    parser = argparse.ArgumentParser(description="UML Calculator CLI")
    parser.add_argument("expression", nargs="?", help="Expression to evaluate")
    parser.add_argument(
        "--mode",
        choices=["auto", "standard", "uml", "ris"],
        default="auto",
        help="Calculation mode",
    )
    parser.add_argument("--steps", action="store_true", help="Show calculation steps")
    args = parser.parse_args()

    if args.expression:
        try:
            result, steps = evaluate_expression(
                args.expression, mode=args.mode, show_steps=args.steps
            )
            if args.steps and steps:
                for step in steps:
                    print(step)
            print_result(args.expression, result, mode=args.mode)
        except Exception as e:
            print(f"Error: {e}")
    else:
        while True:
            try:
                expr = input("UML> ").strip()
                if not expr:
                    continue
                result, steps = evaluate_expression(
                    expr, mode=args.mode, show_steps=args.steps
                )
                if args.steps and steps:
                    for step in steps:
                        print(step)
                print_result(expr, result, mode=args.mode)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting UML Calculator CLI.")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
