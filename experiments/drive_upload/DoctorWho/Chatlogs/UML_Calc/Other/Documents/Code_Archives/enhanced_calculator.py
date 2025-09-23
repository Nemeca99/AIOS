"""
Enhanced UML Calculator with Unified UML/RIS Logic
Integrates all UML/RIS functionality into a single robust calculator system
with improved parsing, fallback handling, and error messages.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import datetime
import math
import time
import re
from typing import Any, Dict, List, Tuple, Optional

# Import our secure evaluation module
from safe_eval import safe_eval

# Import the enhanced UML core with our new functions
from uml_core import (
    parse_uml, eval_uml, eval_recursive_compress, 
    ris_meta_operator, recursive_compress, tfid_anchor,
    validate_magic_square, superposition_collapse,
    letter_to_number, number_to_letter,
    run_enhanced_tests, demo_conversation_insights, print_help,
    convert_standard_to_uml, parse_ris_expression
)

# Import our feature enhancements
from feature_enhancements import (
    roman_to_int, int_to_roman,
    logic_and, logic_or, logic_not, logic_xor,
    set_union, set_intersection, set_difference, set_symmetric_difference,
    parse_date, date_difference, date_add,
    register_custom_operator, get_custom_operator, list_custom_operators,
    demo_roman_numerals, demo_logic_operations, demo_set_operations,
    demo_date_operations, demo_custom_operators
)

# Import symbolic extensions
from symbolic_extensions import (
    base52_encode, base52_decode, apply_si_prefix,
    vector_add, vector_dot, vector_cross, vector_magnitude,
    matrix_multiply, matrix_determinant, matrix_transpose,
    is_prime, prime_factors, gcd, lcm, fibonacci, factorial,
    mean, median, mode, standard_deviation,
    combinations, permutations, EXTENDED_UML_OPERATORS,
    demo_symbolic_extensions
)

class UMLCalculatorGUI:
    """Enhanced Tkinter GUI for UML Calculator with modern styling"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("UML Calculator - Enhanced with T.R.E.E.S. Principles")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.history = []
        self.current_expression = tk.StringVar()
        self.result_var = tk.StringVar(value="0")
        self.mode_var = tk.StringVar(value="standard")
        
        self.setup_styles()
        self.create_widgets()
        self.bind_keyboard()
        
    def setup_styles(self):
        """Configure modern styling"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom styles
        self.style.configure('Title.TLabel', 
                           background='#2c3e50', 
                           foreground='#ecf0f1', 
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Display.TFrame', 
                           background='#34495e', 
                           relief='sunken', 
                           borderwidth=2)
        
        self.style.configure('Button.TButton',
                           font=('Arial', 12),
                           padding=10)
                           
        self.style.configure('Calc.TButton',
                           font=('Arial', 14, 'bold'),
                           padding=15)
    
    def create_widgets(self):
        """Create and layout GUI widgets"""
        # Title
        title_frame = ttk.Frame(self.root, style='Title.TLabel')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(title_frame, text="UML Calculator - Enhanced with Conversation Insights", 
                 style='Title.TLabel').pack()
        ttk.Label(title_frame, text="Universal Mathematical Language with T.R.E.E.S. Principles", 
                 style='Title.TLabel', font=('Arial', 10)).pack()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Calculator
        calc_frame = ttk.LabelFrame(main_frame, text="Calculator", padding=10)
        calc_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Display
        display_frame = ttk.Frame(calc_frame, style='Display.TFrame')
        display_frame.pack(fill='x', pady=(0, 10))
        
        # Expression entry
        ttk.Label(display_frame, text="Expression:", background='#34495e', foreground='#ecf0f1').pack(anchor='w')
        self.expression_entry = ttk.Entry(display_frame, textvariable=self.current_expression, 
                                        font=('Consolas', 14), width=40)
        self.expression_entry.pack(fill='x', pady=2)
        
        # Result display
        ttk.Label(display_frame, text="Result:", background='#34495e', foreground='#ecf0f1').pack(anchor='w')
        result_label = ttk.Label(display_frame, textvariable=self.result_var, 
                               font=('Consolas', 16, 'bold'), 
                               background='#2c3e50', foreground='#e74c3c')
        result_label.pack(fill='x', pady=2)
        
        # Mode selection
        mode_frame = ttk.Frame(calc_frame)
        mode_frame.pack(fill='x', pady=5)
        
        ttk.Label(mode_frame, text="Mode:").pack(side='left')
        ttk.Radiobutton(mode_frame, text="Standard", variable=self.mode_var, 
                       value="standard").pack(side='left', padx=5)
        ttk.Radiobutton(mode_frame, text="UML", variable=self.mode_var, 
                       value="uml").pack(side='left', padx=5)
        ttk.Radiobutton(mode_frame, text="RIS", variable=self.mode_var, 
                       value="ris").pack(side='left', padx=5)
        
        # Button grid
        self.create_button_grid(calc_frame)
        
        # Control buttons
        control_frame = ttk.Frame(calc_frame)
        control_frame.pack(fill='x', pady=5)
        
        ttk.Button(control_frame, text="Calculate", command=self.calculate, 
                  style='Calc.TButton').pack(side='left', padx=2)
        ttk.Button(control_frame, text="Clear", command=self.clear, 
                  style='Button.TButton').pack(side='left', padx=2)
        ttk.Button(control_frame, text="Demo", command=self.show_demo, 
                  style='Button.TButton').pack(side='left', padx=2)
        ttk.Button(control_frame, text="Tests", command=self.run_tests, 
                  style='Button.TButton').pack(side='left', padx=2)
        
        # Right panel - History and Advanced
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # History
        history_frame = ttk.LabelFrame(right_frame, text="History", padding=5)
        history_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=15, 
                                                    font=('Consolas', 10))
        self.history_text.pack(fill='both', expand=True)
        
        # Advanced functions
        advanced_frame = ttk.LabelFrame(right_frame, text="Advanced Functions", padding=5)
        advanced_frame.pack(fill='x')
          # Organize advanced buttons in a grid
        button_frame = ttk.Frame(advanced_frame)
        button_frame.pack(fill='x')
        
        advanced_buttons = [
            ("Vector Ops", self.show_vector_demo),
            ("Matrix Ops", self.show_matrix_demo),
            ("Statistics", self.show_stats_demo),
            ("Number Theory", self.show_number_theory_demo),
            ("Base52", self.show_base52_demo),
            ("SI Prefixes", self.show_si_demo),
            ("RIS Meta-Op", self.ris_demo),
            ("Magic Square", self.magic_square_demo),
            ("Fibonacci", self.show_fibonacci_demo),
            ("Prime Check", self.show_prime_demo),
            ("Recursive Compress", self.compression_demo),
            ("Roman Num", self.show_roman_demo),
            ("Logic Ops", self.show_logic_demo),
            ("Sets", self.show_sets_demo),
            ("Date Calc", self.show_date_demo),
            ("Custom Ops", self.show_custom_ops_demo),
            ("Help", self.show_help)
        ]
        
        # Arrange in 2 columns
        for i, (text, command) in enumerate(advanced_buttons):
            row = i // 2
            col = i % 2
            ttk.Button(button_frame, text=text, command=command, 
                      style='Button.TButton').grid(row=row, column=col, 
                                                   padx=2, pady=2, sticky='ew')
        
        # Configure column weights
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
    
    def create_button_grid(self, parent):
        """Create calculator button grid"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        # Basic calculator buttons
        buttons = [
            ['7', '8', '9', '/', 'AC'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '.', '=', '+', '⌫'],
            ['[', ']', '{', '}', ','],
            ['<', '>', '?', '/', '@'],
            ['A', 'B', 'C', 'z', '!']
        ]
        
        for row_idx, button_row in enumerate(buttons):
            for col_idx, button_text in enumerate(button_row):
                if button_text == '=':
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=self.calculate, width=3)
                elif button_text == 'AC':
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=self.clear, width=3)
                elif button_text == '⌫':
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=self.backspace, width=3)
                else:
                    btn = ttk.Button(button_frame, text=button_text, 
                                   command=lambda t=button_text: self.add_to_expression(t), 
                                   width=3)
                btn.grid(row=row_idx, column=col_idx, padx=1, pady=1)
        
        # Add conversion buttons
        conversion_frame = ttk.LabelFrame(button_frame.master, text="Conversion Tools", padding=5)
        conversion_frame.pack(fill='x', pady=(10, 0))
        
        conversion_buttons = [
            ("Convert to UML", self.convert_to_uml),
            ("Convert to Base52", self.convert_to_base52),
            ("Show UML Steps", self.show_uml_steps),
            ("Arithmetic Test", self.run_arithmetic_tests),
            ("Random Test", self.random_test_suite)
        ]
        
        for i, (text, command) in enumerate(conversion_buttons):
            ttk.Button(conversion_frame, text=text, command=command, 
                      width=15).grid(row=i//3, column=i%3, padx=2, pady=2)
    
    def bind_keyboard(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Delete>', lambda e: self.clear())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.expression_entry.focus_set()
    
    def add_to_expression(self, text):
        """Add text to current expression"""
        current = self.current_expression.get()
        self.current_expression.set(current + text)
        
    def clear(self):
        """Clear the calculator"""
        self.current_expression.set("")
        self.result_var.set("0")
    
    def backspace(self):
        """Remove last character"""
        current = self.current_expression.get()
        self.current_expression.set(current[:-1])
    
    def calculate(self):
        """Calculate the current expression with enhanced parsing and fallback"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
            
        try:
            mode = self.mode_var.get()
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            
            # UML Mode
            if mode == "uml":
                # First try direct UML parsing
                try:
                    parsed = parse_uml(expression)
                    result = eval_uml(parsed)
                    self.result_var.set(f"UML: {result}")
                    history_entry = f"[{timestamp}] UML: {expression} = {result}"
                except Exception:
                    # Try converting standard to UML
                    try:
                        uml_expr = convert_standard_to_uml(expression)
                        # Only if conversion changed something
                        if uml_expr != expression:
                            try:
                                parsed = parse_uml(uml_expr)
                                result = eval_uml(parsed)
                                self.result_var.set(f"UML: {result}")
                                history_entry = f"[{timestamp}] UML: {expression} → {uml_expr} = {result}"
                            except Exception:
                                # Final fallback to standard evaluation
                                try:
                                    result = safe_eval(expression)
                                    self.result_var.set(f"UML: {result}")
                                    history_entry = f"[{timestamp}] UML: {expression} = {result}"
                                except Exception:
                                    self.result_var.set(f"UML Error: Cannot parse {expression}")
                                    return
                        else:
                            # Final fallback to standard evaluation
                            try:
                                result = safe_eval(expression)
                                self.result_var.set(f"UML: {result}")
                                history_entry = f"[{timestamp}] UML: {expression} = {result}"
                            except Exception:
                                self.result_var.set(f"UML Error: Cannot parse {expression}")
                                return
                    except Exception:
                        # Final fallback to standard evaluation
                        try:
                            result = safe_eval(expression)
                            self.result_var.set(f"UML: {result}")
                            history_entry = f"[{timestamp}] UML: {expression} = {result}"
                        except Exception:
                            self.result_var.set(f"UML Error: Cannot parse {expression}")
                            return
              # RIS Mode
            elif mode == "ris":
                # Use enhanced parse_ris_expression function
                try:
                    result, operation = parse_ris_expression(expression)
                    self.result_var.set(f"RIS: {result} via {operation}")
                    history_entry = f"[{timestamp}] RIS: {expression} = {result} via {operation}"
                except ValueError as e:
                    self.result_var.set(f"RIS Value Error: {str(e)}")
                    return
                except SyntaxError as e:
                    self.result_var.set(f"RIS Syntax Error: {str(e)}")
                    return
                except TypeError as e:
                    self.result_var.set(f"RIS Type Error: {str(e)}")
                    return
                except Exception as e:
                    self.result_var.set(f"RIS Error: {str(e)}")
                    return
            
            # Standard Mode
            else:
                # Check for special function patterns
                if expression.startswith('F[') and expression.endswith(']'):
                    # Fibonacci: F[n]
                    n = int(expression[2:-1])
                    result = fibonacci(n)
                    self.result_var.set(f"F({n}) = {result}")
                    history_entry = f"[{timestamp}] Fibonacci {expression} = {result}"
                elif expression.startswith('P[') and expression.endswith(']'):
                    # Prime check: P[n]
                    n = int(expression[2:-1])
                    result = 1 if is_prime(n) else 0
                    status = "prime" if result else "composite"
                    self.result_var.set(f"{n} is {status}")
                    history_entry = f"[{timestamp}] Prime check {expression} = {status}"
                elif expression.startswith('&[') and expression.endswith(']'):                    # GCD: &[a,b]
                    parts = expression[2:-1].split(',')
                    if len(parts) == 2:
                        a, b = int(parts[0]), int(parts[1])
                        result = gcd(a, b)
                        self.result_var.set(f"GCD({a},{b}) = {result}")
                        timestamp = time.strftime("%H:%M:%S")
                        history_entry = f"[{timestamp}] {expression} = {result}"
                    else:
                        self.result_var.set("GCD Error: Use &[a,b]")
                        return
                elif expression.startswith('|[') and expression.endswith(']'):
                    # LCM: |[a,b]
                    parts = expression[2:-1].split(',')
                    if len(parts) == 2:
                        a, b = int(parts[0]), int(parts[1])
                        result = lcm(a, b)
                        self.result_var.set(f"LCM({a},{b}) = {result}")
                        history_entry = f"[{timestamp}] {expression} = {result}"
                    else:
                        self.result_var.set("LCM Error: Use |[a,b]")
                        return
                elif expression.startswith('%[') and expression.endswith(']'):
                    # Modulo: %[a,b]
                    parts = expression[2:-1].split(',')
                    if len(parts) == 2:
                        a, b = float(parts[0]), float(parts[1])
                        if b == 0:
                            self.result_var.set("Modulo Error: Division by zero")
                            return
                        else:
                            result = a % b
                            self.result_var.set(f"{a} mod {b} = {result}")
                            history_entry = f"[{timestamp}] {expression} = {result}"
                    else:
                        self.result_var.set("Modulo Error: Use %[a,b]")
                        return
                elif expression.startswith('R[') and expression.endswith(']'):
                    # Roman numeral: R[2023] or R[MMXXIII]
                    content = expression[2:-1]
                    if content.isdigit():
                        # Convert number to Roman
                        num = int(content)
                        if 1 <= num <= 3999:
                            result = int_to_roman(num)
                            self.result_var.set(f"Roman: {result}")
                            history_entry = f"[{timestamp}] {expression} = {result}"
                        else:
                            self.result_var.set("Roman Error: Must be 1-3999")
                            return
                    else:
                        # Convert Roman to number
                        try:
                            result = roman_to_int(content)
                            self.result_var.set(f"Decimal: {result}")
                            history_entry = f"[{timestamp}] {expression} = {result}"
                        except ValueError as e:
                            self.result_var.set(f"Roman Error: {str(e)}")
                            return
                            
                # Logic operations
                elif expression.startswith('AND[') and expression.endswith(']'):
                    # Logic AND: AND[1,0,1]
                    content = expression[4:-1]
                    values = [int(x.strip()) for x in content.split(',')]
                    result = logic_and(values)
                    self.result_var.set(f"AND: {result}")
                    history_entry = f"[{timestamp}] {expression} = {result}"
                    
                elif expression.startswith('OR[') and expression.endswith(']'):
                    # Logic OR: OR[1,0,1]
                    content = expression[3:-1]
                    values = [int(x.strip()) for x in content.split(',')]
                    result = logic_or(values)
                    self.result_var.set(f"OR: {result}")
                    history_entry = f"[{timestamp}] {expression} = {result}"
                    
                elif expression.startswith('NOT[') and expression.endswith(']'):
                    # Logic NOT: NOT[1]
                    content = expression[4:-1]
                    values = [int(x.strip()) for x in content.split(',')]
                    try:
                        result = logic_not(values)
                        self.result_var.set(f"NOT: {result}")
                        history_entry = f"[{timestamp}] {expression} = {result}"
                    except ValueError as e:
                        self.result_var.set(f"NOT Error: {str(e)}")
                        return
                        
                elif expression.startswith('XOR[') and expression.endswith(']'):
                    # Logic XOR: XOR[1,0,1]
                    content = expression[4:-1]
                    values = [int(x.strip()) for x in content.split(',')]
                    result = logic_xor(values)
                    self.result_var.set(f"XOR: {result}")
                    history_entry = f"[{timestamp}] {expression} = {result}"
                else:
                    # Try standard evaluation first
                    try:
                        result = safe_eval(expression)
                        self.result_var.set(str(result))
                        history_entry = f"[{timestamp}] {expression} = {result}"
                    except ValueError as e:
                        self.result_var.set(f"Value Error: {str(e)}")
                    except SyntaxError as e:
                        self.result_var.set(f"Syntax Error: {str(e)}")
                    except TypeError as e:
                        self.result_var.set(f"Type Error: {str(e)}")
                        # Fall back to UML parsing
                        try:
                            parsed = parse_uml(expression)
                            result = eval_uml(parsed)
                            self.result_var.set(str(result))
                            history_entry = f"[{timestamp}] {expression} = {result}"
                        except ValueError as e:
                            self.result_var.set(f"UML Value Error: {str(e)}")
                            return
                        except SyntaxError as e:
                            self.result_var.set(f"UML Syntax Error: {str(e)}")
                            return
                        except TypeError as e:
                            self.result_var.set(f"UML Type Error: {str(e)}")
                            return
                        except Exception as e:
                            self.result_var.set(f"UML Error: {str(e)}")
                            return
            
            # Add to history
            self.history.append(history_entry)
            self.update_history_display()
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
            
    def update_history_display(self):
        """Update the history text widget"""
        self.history_text.delete(1.0, tk.END)
        for entry in self.history[-20:]:  # Show last 20 entries
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
    
    # === CONVERSION METHODS ===
    
    def convert_to_uml(self):
        """Convert current expression to UML format using our enhanced converter"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
        
        try:
            # Use our enhanced converter
            uml_expr = convert_standard_to_uml(expression)
            if uml_expr != expression:
                self.current_expression.set(uml_expr)
                
                # Show the expected result
                try:
                    result = eval_recursive_compress(uml_expr)
                    self.result_var.set(f"UML: {result}")
                    
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    history_entry = f"[{timestamp}] Converted {expression} → {uml_expr} = {result}"
                    self.history.append(history_entry)
                    self.update_history_display()
                except Exception as e:
                    self.result_var.set(f"UML: Cannot evaluate {uml_expr}")
            else:
                self.result_var.set("Already in UML format or no conversion possible")
                
        except Exception as e:
            self.result_var.set(f"Conversion Error: {str(e)}")
    
    def convert_to_base52(self):
        """Convert current expression to Base52 format"""
        expression = self.current_expression.get().strip()
        if not expression:            return
        
        try:
            # Parse and evaluate the expression first
            result = safe_eval(expression)
            
            # Convert numbers in expression to Base52
            import re
            
            # Find all numbers in the expression
            numbers = re.findall(r'\d+(?:\.\d+)?', expression)
            
            if numbers:
                # Convert each number to Base52
                base52_numbers = []
                for num_str in numbers:
                    num = int(float(num_str))  # Convert to int for Base52
                    try:
                        if num > 0:
                            base52_num = base52_encode(num)
                            base52_numbers.append(base52_num)
                        else:
                            base52_numbers.append(str(num))
                            self.result_var.set(f"Note: Base52 only encodes positive integers, keeping {num} as-is")
                    except ValueError as e:
                        base52_numbers.append(str(num))
                        self.result_var.set(f"Base52 error: {str(e)}")
                
                # Convert result to Base52 too
                result_int = int(result) if isinstance(result, (int, float)) and result > 0 else result
                result_base52 = base52_encode(result_int) if isinstance(result_int, int) and result_int > 0 else str(result)
                
                # Create Base52 UML expression
                if len(base52_numbers) >= 2:
                    base52_expr = f"[{','.join(base52_numbers)}]"
                    self.current_expression.set(base52_expr)
                    self.result_var.set(f"Base52: {result_base52}")
                    
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    history_entry = f"[{timestamp}] Base52: {expression} → {base52_expr} = {result_base52}"
                    self.history.append(history_entry)
                    self.update_history_display()
                else:
                    self.result_var.set("Need at least 2 numbers for Base52 conversion")
            else:
                self.result_var.set("No numbers found to convert to Base52")
                
        except Exception as e:
            self.result_var.set(f"Base52 Error: {str(e)}")
    
    def show_uml_steps(self):
        """Show step-by-step UML parsing and evaluation"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
        
        try:
            steps = []
            steps.append(f"Original expression: {expression}")
            
            # Try standard to UML conversion
            try:
                uml_expr = convert_standard_to_uml(expression)
                if uml_expr != expression:
                    steps.append(f"Converted to UML: {uml_expr}")
                    expression = uml_expr
            except Exception as e:
                steps.append(f"UML conversion failed: {e}")
            
            # Try standard evaluation first
            try:
                result = safe_eval(expression)
                steps.append(f"Standard evaluation: {result}")
            except Exception as e:
                steps.append(f"Standard evaluation failed: {e}")
            
            # Try UML parsing
            try:
                parsed = parse_uml(expression)
                steps.append(f"UML parsed: {parsed}")
                
                uml_result = eval_uml(parsed)
                steps.append(f"UML evaluation: {uml_result}")
            except Exception as e:
                steps.append(f"UML parsing failed: {e}")
            
            # Try recursive compression
            try:
                compressed = eval_recursive_compress(expression)
                steps.append(f"Recursive compression: {compressed}")
            except Exception as e:
                steps.append(f"Recursive compression failed: {e}")
            
            # Try RIS meta-operator if appropriate
            if ',' in expression or '+' in expression or '-' in expression or '*' in expression or '/' in expression:
                try:
                    result, operation = parse_ris_expression(expression)
                    steps.append(f"RIS meta-operator: {result} via {operation}")
                except Exception as e:
                    steps.append(f"RIS meta-operator failed: {e}")
            
            # Show steps in a new window
            steps_text = "\n".join(steps)
            self.show_text_window("UML Processing Steps", steps_text)
            
        except Exception as e:
            self.result_var.set(f"Steps Error: {str(e)}")
    
    def run_arithmetic_tests(self):
        """Run comprehensive arithmetic tests across all modes"""
        test_cases = [
            "7+7", "1+1", "2*3", "10-4", "15/3",
            "2+3*4", "(5+3)*2", "100/10+5",
            "7*7", "9-5", "20/4", "3*3*3"        ]
        results = []
        results.append("=== ARITHMETIC TEST SUITE ===\n")
        
        for expr in test_cases:
            results.append(f"Testing: {expr}")
            
            # Standard mode
            try:
                std_result = safe_eval(expr)
                results.append(f"  Standard: {std_result}")
            except Exception as e:
                results.append(f"  Standard: Error - {e}")
            
            # UML mode - first try direct UML parsing
            try:
                uml_expr = convert_standard_to_uml(expr)
                uml_result = eval_recursive_compress(uml_expr)
                results.append(f"  UML: {uml_result} (converted to {uml_expr})")
            except Exception as e:
                try:
                    # Try direct parsing as fallback
                    uml_result = eval_recursive_compress(expr)
                    results.append(f"  UML: {uml_result}")
                except Exception as e2:
                    results.append(f"  UML: Error - Cannot parse")
            
            # RIS mode
            try:
                ris_result, operation = parse_ris_expression(expr)
                results.append(f"  RIS: {ris_result} via {operation}")
            except Exception as e:
                results.append(f"  RIS: Not applicable")
            
            results.append("")  # Empty line
        
        # Show results
        self.show_text_window("Arithmetic Test Results", "\n".join(results))
    
    def random_test_suite(self):
        """Run randomized test cases"""
        import random
        
        results = []
        results.append("=== RANDOM TEST SUITE ===\n")
        
        # Generate random test cases
        for i in range(10):
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            op = random.choice(['+', '-', '*', '/'])
            
            if op == '/' and b == 0:
                b = 1  # Avoid division by zero
            
            expr = f"{a}{op}{b}"
            results.append(f"Test {i+1}: {expr}")
            
            # Test all modes
            try:
                std_result = safe_eval(expr)
                results.append(f"  Standard: {std_result}")
                
                uml_expr = convert_standard_to_uml(expr)
                uml_result = eval_recursive_compress(uml_expr)
                results.append(f"  UML: {uml_result} (as {uml_expr})")
                
                ris_result, operation = parse_ris_expression(expr)
                results.append(f"  RIS: {ris_result} via {operation}")
                
                # Base52 conversion
                base52_a = base52_encode(a)
                base52_b = base52_encode(b)
                base52_result = base52_encode(int(std_result)) if isinstance(std_result, (int, float)) and std_result > 0 else str(std_result)
                results.append(f"  Base52: [{base52_a},{base52_b}] = {base52_result}")
                
            except Exception as e:
                results.append(f"  Error: {e}")
            
            results.append("")  # Empty line
            
        # Show results
        self.show_text_window("Random Test Results", "\n".join(results))
    
    # === DEMO METHODS ===
    
    def show_demo(self):
        """Show UML/RIS demo with examples"""
        demo_text = """
=== UML Calculator Demo ===

UML (Universal Mathematical Language) is a symbolic mathematical notation system
with dimensional bracket operators and recursive evaluation.

Examples:
  [2,3]           = 5      (Addition)
  {10,4}          = 6      (Subtraction)
  <3,4>           = 12     (Multiplication)
  <>10,2<>        = 5      (Division)
  [A,B,C]         = 6      (Using base-52 letters: A=1, B=2, C=3)
  /9<             = 3      (Square root)
  ?(2,8)          = 3      (Log base 2 of 8)
  <[1,2],3>       = 9      (Nested expressions: (1+2)×3)
  
RIS (Recursive Integration System) applies all operations simultaneously
and selects the one that produces the simplest result:

  RIS(6,2)        = 4      (via subtraction)
  RIS(10,5)       = 2      (via division)
  RIS(2,8)        = 16     (via multiplication)
  
Try these examples in the calculator!
"""
        self.show_text_window("UML/RIS Demo", demo_text)
    
    def run_tests(self):
        """Run the enhanced test suite"""
        # Start test in a separate thread to keep UI responsive
        threading.Thread(target=self._run_tests_thread, daemon=True).start()
    
    def _run_tests_thread(self):
        """Run tests in background thread"""
        # Capture output
        import io
        import sys
        old_stdout = sys.stdout
        result_capture = io.StringIO()
        sys.stdout = result_capture
        
        # Run tests
        run_enhanced_tests()
        
        # Restore stdout
        sys.stdout = old_stdout
        
        # Show results in UI
        self.root.after(0, lambda: self.show_text_window("UML Test Results", result_capture.getvalue()))

    def ris_demo(self):
        """RIS meta-operator demo"""
        demo_text = """
=== RIS Meta-Operator Demo ===

RIS (Recursive Integration System) performs all basic operations (+, -, *, /)
simultaneously and collapses the superposition to the simplest result.

The "simplicity" is determined by entropy - the result with minimal
information complexity wins.

Examples:
"""
        # Add live examples
        test_pairs = [(6, 2), (10, 5), (8, 4), (2, 16), (7, 2), (12, 4)]
        for a, b in test_pairs:
            result, operation = ris_meta_operator(a, b)
            demo_text += f"\n  RIS({a}, {b}) = {result} via {operation}"
            
            # Add entropy explanation
            if operation == 'add':
                demo_text += f" (Addition is simplest: {a}+{b}={result})"
            elif operation == 'sub':
                demo_text += f" (Subtraction is simplest: {a}-{b}={result})"
            elif operation == 'mul':
                demo_text += f" (Multiplication is simplest: {a}×{b}={result})"
            elif operation == 'div':
                demo_text += f" (Division is simplest: {a}÷{b}={result})"
        
        # Add more explanation
        demo_text += """

Why is this useful?

The RIS meta-operator is a key part of the T.R.E.E.S. principles:
- It allows mathematical expressions to find their own minimal entropy path
- It parallels quantum superposition and collapse
- It enables recursive compression of complex expressions

Try entering expressions in RIS mode, or explicitly use @(a,b) notation.
"""
        self.show_text_window("RIS Meta-Operator Demo", demo_text)
    
    def compression_demo(self):
        """Recursive compression demo"""
        demo_text = """
=== Recursive Compression Demo ===

Recursive compression stabilizes exponential growth and makes large 
values more manageable using the formula:

    f(a) = a / (1 + log(a+1))

Examples:
"""
        # Add live examples
        test_values = [10, 100, 1000, 10000, 100000, 1000000]
        for val in test_values:
            compressed = recursive_compress(val)
            reduction = (1 - compressed/val) * 100
            demo_text += f"\n  {val:,} → {compressed:.4f} ({reduction:.1f}% reduction)"
        
        # Add more explanation
        demo_text += """

Why is this useful?

- Prevents overflow in exponential calculations
- Creates stable memory structures in recursive systems
- Helps identify entropy-minimized states in complex functions
- Forms the foundation of T.R.E.E.S. information architecture

The calculator automatically applies recursive compression when results
would otherwise be too large to manage.
"""
        self.show_text_window("Recursive Compression Demo", demo_text)

    def show_vector_demo(self):
        """Vector operations demo"""
        demo_text = """
=== Vector Operations Demo ===

The UML Calculator supports vector operations through symbolic extensions:

Vector Addition: [1,2,3] + [4,5,6]
"""
        # Add a live calculation
        v1 = [1, 2, 3]
        v2 = [4, 5, 6]
        demo_text += f"  Result: {vector_add(v1, v2)}\n\n"
        
        demo_text += "Vector Dot Product: [1,2,3] · [4,5,6]"
        demo_text += f"\n  Result: {vector_dot(v1, v2)}\n\n"
        
        demo_text += "Vector Cross Product: [1,2,3] × [4,5,6]"
        demo_text += f"\n  Result: {vector_cross(v1, v2)}\n\n"
        
        demo_text += "Vector Magnitude: |[1,2,3]|"
        demo_text += f"\n  Result: {vector_magnitude(v1):.4f}\n\n"
        
        demo_text += """
To use vector operations in the calculator:
1. Enter vectors in array format: [1,2,3]
2. Use vector_add(), vector_dot(), etc. functions
3. Combine with UML operations for complex calculations
"""
        self.show_text_window("Vector Operations Demo", demo_text)
    
    def show_matrix_demo(self):
        """Matrix operations demo"""
        demo_text = """
=== Matrix Operations Demo ===

The UML Calculator supports matrix operations through symbolic extensions:

Matrix Multiplication:
  [[1,2],[3,4]] × [[5,6],[7,8]]
"""
        # Add a live calculation
        m1 = [[1, 2], [3, 4]]
        m2 = [[5, 6], [7, 8]]
        demo_text += f"  Result: {matrix_multiply(m1, m2)}\n\n"
        
        demo_text += "Matrix Determinant: det([[1,2],[3,4]])"
        demo_text += f"\n  Result: {matrix_determinant(m1)}\n\n"
        
        demo_text += "Matrix Transpose: [[1,2],[3,4]]ᵀ"
        demo_text += f"\n  Result: {matrix_transpose(m1)}\n\n"
        
        demo_text += """
To use matrix operations in the calculator:
1. Enter matrices as nested arrays: [[1,2],[3,4]]
2. Use matrix_multiply(), matrix_determinant(), etc. functions
3. Combine with UML operations for linear algebra calculations
"""
        self.show_text_window("Matrix Operations Demo", demo_text)
    
    def show_stats_demo(self):
        """Statistics demo"""
        data = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9]
        demo_text = f"""
=== Statistics Functions Demo ===

The UML Calculator includes statistical functions for data analysis.

Sample data: {data}

Mean: {mean(data):.2f}
Median: {median(data):.1f}
Mode: {mode(data)}
Standard Deviation: {standard_deviation(data):.3f}

To use statistics functions in the calculator:
1. Create a list of values: [1,2,3,4,5]
2. Use mean(), median(), mode(), standard_deviation()
3. Combine with UML operations for complex analysis
"""
        self.show_text_window("Statistics Demo", demo_text)

    def show_number_theory_demo(self):
        """Number theory demo"""
        demo_text = """
=== Number Theory Demo ===

The UML Calculator includes number theory functions:

Prime Factorization of 60:"""
        demo_text += f"\n  Result: {prime_factors(60)}\n\n"
        
        demo_text += "GCD of 48 and 18:"
        demo_text += f"\n  Result: {gcd(48, 18)}\n\n"
        
        demo_text += "LCM of 12 and 15:"
        demo_text += f"\n  Result: {lcm(12, 15)}\n\n"
        
        demo_text += "Prime Check: Is 17 prime?"
        demo_text += f"\n  Result: {is_prime(17)}\n\n"
        
        demo_text += """
To use number theory functions in the calculator:
1. Call functions directly: prime_factors(60)
2. Use special notation: &[48,18] for GCD, |[12,15] for LCM
3. Use P[17] to check if a number is prime
"""
        self.show_text_window("Number Theory Demo", demo_text)

    def show_base52_demo(self):
        """Base52 encoding demo"""
        demo_text = """
=== Base52 Encoding Demo ===

The UML Calculator supports base-52 encoding where:
- A=1, B=2, ..., Z=26
- a=27, b=28, ..., z=52

Examples:"""
        
        test_values = [(1, 'A'), (26, 'Z'), (27, 'a'), (52, 'z'), (53, 'AA')]
        for num, encoded in test_values:
            demo_text += f"\n  {num} ↔ {base52_encode(num)}"
        
        demo_text += "\n\nYou can use base-52 in UML expressions:"
        demo_text += "\n  [A,B,C] = 6 (1+2+3)"
        demo_text += "\n  <A,z> = 52 (1×52)"
        demo_text += "\n  {Z,A} = 25 (26-1)"
        
        demo_text += """

To use base-52 in the calculator:
1. Enter letters directly in UML expressions
2. Use the "Convert to Base52" button to encode numbers
3. Letters are automatically decoded during evaluation
"""
        self.show_text_window("Base52 Demo", demo_text)

    def show_si_demo(self):
        """SI prefixes demo"""
        demo_text = """
=== SI Prefixes Demo ===

The UML Calculator supports SI prefixes for scientific notation:

k (kilo) = 10³
M (mega) = 10⁶
G (giga) = 10⁹
T (tera) = 10¹²
m (milli) = 10⁻³
u (micro) = 10⁻⁶
n (nano) = 10⁻⁹
p (pico) = 10⁻¹²

Examples:"""
        
        test_values = [('5k', 5000), ('3.2M', 3200000), ('1.5m', 0.0015)]
        for expr, val in test_values:
            demo_text += f"\n  {expr} = {apply_si_prefix(float(expr[:-1]), expr[-1])}"
        
        demo_text += """

To use SI prefixes in the calculator:
1. Enter a number followed by the prefix: 5k, 3.2M, etc.
2. Use apply_si_prefix() function for explicit conversion
3. Combine with UML operations for scientific calculations
"""
        self.show_text_window("SI Prefixes Demo", demo_text)

    def magic_square_demo(self):
        """Magic square demo"""
        # Define a sample magic square
        magic_square = [
            [8, 1, 6],
            [3, 5, 7],
            [4, 9, 2]
        ]
        
        # Validate the magic square
        validation = validate_magic_square(magic_square)
        
        demo_text = """
=== Magic Square Demo ===

The UML Calculator has built-in magic square validation using
T.R.E.E.S. principles and recursive compression.

Example Magic Square:
  8 1 6
  3 5 7
  4 9 2

Magic constant: 15

Validation results:
"""
        # Show validation results
        demo_text += f"  Unique values: {validation['unique']}\n"
        demo_text += f"  Perfect squares: {validation['perfect_squares']}\n"
        demo_text += f"  Line sum uniformity: {validation['line_sum_uniform']}\n"
        demo_text += f"  Center value: {validation['center']}\n"
        demo_text += f"  Target sum: {validation['target_sum']}\n"
        demo_text += f"  Entropy score: {validation['entropy_score']:.6f}\n"
        demo_text += f"  Recursive compression: {validation['recursive_compression']:.6f}\n"
        
        demo_text += """
Magic squares have numerous applications in UML:
- Demonstrate recursive compression principles
- Test entropy minimization algorithms
- Validate T.R.E.E.S. mathematical structures
- Serve as stable reference patterns in RIS operations

To validate your own magic squares, use the validate_magic_square() function.
"""
        self.show_text_window("Magic Square Demo", demo_text)

    def show_fibonacci_demo(self):
        """Fibonacci sequence demo"""
        demo_text = """
=== Fibonacci Sequence Demo ===

The UML Calculator includes Fibonacci sequence generation:

F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2) for n > 1

First 15 Fibonacci numbers:"""
        
        # Generate Fibonacci sequence
        for i in range(15):
            demo_text += f"\n  F({i}) = {fibonacci(i)}"
        
        demo_text += """

There's a strong connection between Fibonacci numbers and UML:
- Fibonacci growth exemplifies patterns that benefit from recursive compression
- The golden ratio (φ ≈ 1.618) emerges from the sequence as a limit
- Fibonacci patterns appear in many RIS collapse states

To use Fibonacci in the calculator:
1. Use fibonacci() function directly
2. Use F[n] notation (e.g., F[10])
3. Try recursive compression on large Fibonacci values
"""
        self.show_text_window("Fibonacci Demo", demo_text)

    def show_prime_demo(self):
        """Prime number demo"""
        demo_text = """
=== Prime Number Demo ===

The UML Calculator includes prime number functions:

Is a number prime?"""
        
        # Show some prime checks
        test_numbers = [7, 10, 17, 20, 23]
        for n in test_numbers:
            demo_text += f"\n  {n}: {'Prime' if is_prime(n) else 'Not prime'}"
        
        demo_text += "\n\nPrime factorization:"
        for n in [12, 30, 45, 97]:
            demo_text += f"\n  {n}: {prime_factors(n)}"
        
        demo_text += """

Prime numbers have special significance in UML:
- They form the basis of the recursive number theory
- Serve as entropy anchors in RIS operations
- Create stable patterns in T.R.E.E.S. architecture

To use prime functions in the calculator:
1. Use is_prime() to check if a number is prime
2. Use P[n] notation for prime check (returns 1 or 0)
3. Use prime_factors() to get prime factorization
"""
        self.show_text_window("Prime Number Demo", demo_text)

    def show_help(self):
        """Show comprehensive help information"""
        help_text = """
=== UML Calculator Help ===
Universal Mathematical Language - Enhanced with T.R.E.E.S. principles

Basic Operations:
  [a,b,c]     Addition (1D forward motion, growth)
  {a,b,c}     Subtraction (1D reverse motion, negation) 
  <a,b,c>     Multiplication (2D expansion, tessellation)
  <>a,b<>     Division (4D recursion, folding, superposition)
  /x<         Square root (recursive collapse)
  ?(a,b)      Logarithm base a of b (recursive compression)

Advanced Features:
  @(a,b)      RIS meta-operator (superposition & entropy collapse)
  (expr)      Priority grouping
  A-Z         Letters = 1-26 (base-52 encoding)
  a-z         Letters = 27-52 (base-52 encoding)

Extended Functions:
  F[n]        nth Fibonacci number
  P[n]        Prime check (1 if prime, 0 if not)
  &[a,b]      Greatest Common Divisor
  |[a,b]      Least Common Multiple
  %[a,b]      Modulo (a mod b)
  ![n]        Factorial (n!)

Conversion Tools:
  - Convert to UML: Translates standard notation to UML brackets
  - Convert to Base52: Encodes numbers as letters
  - Show UML Steps: Shows detailed calculation steps
  - Arithmetic Test: Runs comprehensive tests across modes
  - Random Test: Generates random calculations for testing

Calculator Modes:
  - Standard: Traditional arithmetic with extended functions
  - UML: Universal Mathematical Language notation
  - RIS: Recursive Integration System meta-operator

Demo Functions:
  Access specialized demos through the Advanced Functions panel.
  Each demo provides examples and explanations of calculator features.

Tips:
  - Press Enter to calculate
  - Use backspace to correct mistakes
  - Use clear (AC) to reset
  - Keep the history for reference
  - Try the "Show UML Steps" button to see how calculations work

Key Insight: "Traditional math uses linearity and PEMDAS; 
RIS uses nesting, identity compression, and recursive resolution."
"""
        self.show_text_window("UML Calculator Help", help_text)
    
    def show_text_window(self, title, text):
        """Show a text in a new window"""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("600x400")
        txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Consolas", 10))
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, text)
        txt.config(state=tk.DISABLED)
    
    def show_roman_demo(self):
        """Show Roman numeral conversion demo"""
        try:
            expression = self.current_expression.get().strip()
            if expression.isdigit():
                num = int(expression)
                if 1 <= num <= 3999:
                    roman = int_to_roman(num)
                    self.result_var.set(f"Roman: {roman}")
                else:
                    self.result_var.set("Roman: Must be 1-3999")
            else:
                # Try to interpret as Roman
                try:
                    num = roman_to_int(expression)
                    self.result_var.set(f"Decimal: {num}")
                except ValueError:
                    # Show demo instead
                    self.show_text_demo(demo_roman_numerals, "Roman Numeral Conversion")
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
            
    def show_logic_demo(self):
        """Show logic operations demo"""
        try:
            expression = self.current_expression.get().strip()
            if expression.startswith("AND[") and expression.endswith("]"):
                # AND[1,0,1]
                content = expression[4:-1]
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_and(values)
                self.result_var.set(f"AND: {result}")
            elif expression.startswith("OR[") and expression.endswith("]"):
                # OR[1,0,1]
                content = expression[3:-1]
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_or(values)
                self.result_var.set(f"OR: {result}")
            elif expression.startswith("NOT[") and expression.endswith("]"):
                # NOT[1]
                content = expression[4:-1]
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_not(values)
                self.result_var.set(f"NOT: {result}")
            elif expression.startswith("XOR[") and expression.endswith("]"):
                # XOR[1,0,1]
                content = expression[4:-1]
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_xor(values)
                self.result_var.set(f"XOR: {result}")
            else:
                # Show demo
                self.show_text_demo(demo_logic_operations, "Logic Operations")
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
    
    def show_sets_demo(self):
        """Show set operations demo"""
        try:
            expression = self.current_expression.get().strip()
            if expression.lower().startswith("union[") and expression.endswith("]"):
                self.parse_and_evaluate_set_op(expression, "union")
            elif expression.lower().startswith("intersect[") and expression.endswith("]"):
                self.parse_and_evaluate_set_op(expression, "intersect")
            elif expression.lower().startswith("diff[") and expression.endswith("]"):
                self.parse_and_evaluate_set_op(expression, "diff")
            elif expression.lower().startswith("symdiff[") and expression.endswith("]"):
                self.parse_and_evaluate_set_op(expression, "symdiff")
            else:
                # Show demo
                self.show_text_demo(demo_set_operations, "Set Operations")
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
    
    def parse_and_evaluate_set_op(self, expression, op_type):
        """Parse a set operation expression and evaluate it"""
        import re
        # Extract the content between square brackets
        match = re.match(r'[A-Za-z]+\[(.*)\]', expression)
        if not match:
            raise ValueError("Invalid set operation format")
        
        content = match.group(1)
        # Split by semicolons for multiple sets
        sets_str = content.split(';')
        
        # Parse each set (comma-separated values)
        sets = []
        for set_str in sets_str:
            # Handle empty set
            if set_str.strip() == '':
                sets.append([])
                continue
                
            # Parse set elements - try to convert to appropriate types
            elements = []
            for elem in set_str.split(','):
                elem = elem.strip()
                if elem.isdigit():
                    elements.append(int(elem))
                elif elem.replace('.', '', 1).isdigit():
                    elements.append(float(elem))
                else:
                    elements.append(elem)
            sets.append(elements)
        
        # Apply the operation
        if op_type == "union":
            result = set_union(sets)
            self.result_var.set(f"Union: {result}")
        elif op_type == "intersect":
            result = set_intersection(sets)
            self.result_var.set(f"Intersection: {result}")
        elif op_type == "diff":
            result = set_difference(sets)
            self.result_var.set(f"Difference: {result}")
        elif op_type == "symdiff":
            result = set_symmetric_difference(sets)
            self.result_var.set(f"Symmetric Difference: {result}")
    
    def show_date_demo(self):
        """Show date calculation demo"""
        try:
            expression = self.current_expression.get().strip()
            if expression.lower().startswith("datediff[") and expression.endswith("]"):
                # Format: datediff[2023-01-01;2023-12-31]
                content = expression[9:-1]
                dates = content.split(';')
                if len(dates) != 2:
                    self.result_var.set("Date Error: Use datediff[YYYY-MM-DD;YYYY-MM-DD]")
                    return
                    
                try:
                    date1, date2 = dates
                    days = date_difference(date1.strip(), date2.strip())
                    self.result_var.set(f"Date Difference: {days} days")
                    timestamp = time.strftime("%H:%M:%S")
                    history_entry = f"[{timestamp}] {expression} = {days} days"
                except Exception as e:
                    self.result_var.set(f"Date Error: {str(e)}")
                    return
                
            elif expression.lower().startswith("dateadd[") and expression.endswith("]"):
                # Format: dateadd[2023-01-01;30]
                content = expression[8:-1]
                parts = content.split(';')
                if len(parts) != 2:
                    self.result_var.set("Date Error: Use dateadd[YYYY-MM-DD;days]")
                    return
                    
                try:
                    date_str, days_str = parts
                    days = int(days_str)
                    result_date = date_add(date_str.strip(), days)
                    self.result_var.set(f"Date + {days} days = {result_date}")
                    timestamp = time.strftime("%H:%M:%S")
                    history_entry = f"[{timestamp}] {expression} = {result_date}"
                except Exception as e:
                    self.result_var.set(f"Date Error: {str(e)}")
                    return
            else:
                # Show demo
                self.show_text_demo(demo_date_operations, "Date Operations")
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
    
    def show_custom_ops_demo(self):
        """Show custom operators demo"""
        try:
            expression = self.current_expression.get().strip()
            if expression.lower().startswith("register[") and expression.endswith("]"):
                # This is more of a placeholder since defining custom operators
                # through the GUI requires Python code evaluation which is unsafe
                # In a real implementation, this would use a safer approach
                self.result_var.set("Custom operators can't be defined through GUI")
                
            elif expression.lower() == "listops":
                ops = list_custom_operators()
                if ops:
                    self.result_var.set(f"Custom ops: {', '.join(ops)}")
                else:
                    self.result_var.set("No custom operators registered")
                    
            else:
                # Show demo
                self.show_text_demo(demo_custom_operators, "Custom Operators")
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
            
    def show_text_demo(self, demo_func, title):
        """Show a demo in a popup window"""
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("500x400")
        popup.configure(bg='#2c3e50')
        
        # Redirect stdout to capture demo output
        import io
        import sys
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        # Run the demo function
        demo_func()
        
        # Get the output and restore stdout
        output = new_stdout.getvalue()
        sys.stdout = old_stdout
        
        # Show the output in a scrolled text widget
        text = scrolledtext.ScrolledText(popup, font=('Consolas', 10))
        text.pack(fill='both', expand=True, padx=10, pady=10)
        text.insert(tk.END, output)
        text.configure(state='disabled')
        
        # Close button
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=5)
        
def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python enhanced_calculator.py [gui|test <expr>]")
        print("  gui  - Launch desktop calculator GUI")
        print("  test <expr> - Evaluate an expression in all modes")
        return
    
    mode = sys.argv[1].lower()
    if mode == "gui":
        app = UMLCalculatorGUI()
        app.root.mainloop()
    elif mode == "test":
        if len(sys.argv) < 3:
            print("Usage: python enhanced_calculator.py test <expr>")
            return
            
        expr = sys.argv[2]
        
        # Standard mode
        try:
            print(f"Standard: {expr} = {safe_eval(expr)}")
        except Exception as e:
            print(f"Standard: {expr} = Error: {e}")
        
        # UML mode
        try:
            # First try direct parsing
            try:
                parsed = parse_uml(expr)
                result = eval_uml(parsed)
                print(f"UML: {expr} = {result}")
            except Exception:
                # Try with conversion
                uml_expr = convert_standard_to_uml(expr)
                if uml_expr != expr:
                    parsed = parse_uml(uml_expr)
                    result = eval_uml(parsed)
                    print(f"UML: {expr} = {result} (converted to {uml_expr})")
                else:
                    raise # Re-raise to hit the broader exception handler
        except Exception as e:
            print(f"UML: {expr} = Error: {e}")
        
        # RIS mode
        try:
            result, operation = parse_ris_expression(expr)
            print(f"RIS: {expr} = {result} via {operation}")
        except Exception as e:
            print(f"RIS: {expr} = Error: {e}")
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python enhanced_calculator.py [gui|test <expr>]")

if __name__ == "__main__":
    main()
