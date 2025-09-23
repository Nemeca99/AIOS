"""
Enhanced UML Calculator with Multiple Interfaces
Integrates the enhanced UML core with modern UI options including Tkinter desktop app and enhanced CLI. All built on the conversation-analysis-enhanced
UML core with RIS meta-operator, recursive compression, and T.R.E.E.S. principles.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import datetime
import math
import time
from typing import Any, Dict, List, Tuple, Optional

# Import the enhanced UML core
from uml_core import (
    parse_uml, eval_uml, eval_recursive_compress, 
    ris_meta_operator, recursive_compress, tfid_anchor,
    validate_magic_square, superposition_collapse,
    letter_to_number, number_to_letter,
    run_enhanced_tests, demo_conversation_insights, print_help,
    convert_standard_to_uml  # Added new utility function
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
        self.history_text.pack(fill='both', expand=True)        # Advanced functions
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
        """Calculate the current expression"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
            
        try:
            mode = self.mode_var.get()
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            
            # UML Mode
            if mode == "uml":
                # Try direct UML parsing first
                try:
                    parsed = parse_uml(expression)
                    result = eval_uml(parsed)
                    self.result_var.set(f"UML: {result}")
                    history_entry = f"[{timestamp}] UML: {expression} = {result}"
                except Exception:
                    # Try to convert standard arithmetic to UML notation
                    try:
                        uml_expr = convert_standard_to_uml(expression)
                        if uml_expr != expression:
                            try:
                                parsed = parse_uml(uml_expr)
                                result = eval_uml(parsed)
                                self.result_var.set(f"UML: {result}")
                                history_entry = f"[{timestamp}] UML: {expression} → {uml_expr} = {result}"
                            except Exception:
                                # Final fallback to standard evaluation
                                try:
                                    result = eval(expression)
                                    self.result_var.set(f"UML: {result}")
                                    history_entry = f"[{timestamp}] UML: {expression} = {result}"
                                except Exception:
                                    self.result_var.set(f"UML Error: Cannot parse {expression}")
                                    return
                        else:
                            # Final fallback to standard evaluation
                            try:
                                result = eval(expression)
                                self.result_var.set(f"UML: {result}")
                                history_entry = f"[{timestamp}] UML: {expression} = {result}"
                            except Exception:
                                self.result_var.set(f"UML Error: Cannot parse {expression}")
                                return
                    except Exception:
                        # Final fallback to standard evaluation
                        try:
                            result = eval(expression)
                            self.result_var.set(f"UML: {result}")
                            history_entry = f"[{timestamp}] UML: {expression} = {result}"
                        except Exception:
                            self.result_var.set(f"UML Error: Cannot parse {expression}")
                            return
            
            # RIS Mode
            elif mode == "ris":
                # Try RIS notation like @(a,b) first
                if expression.startswith('@(') and expression.endswith(')'):
                    try:
                        # Extract values from @(a,b) notation
                        inner = expression[2:-1]
                        parts = inner.split(',')
                        if len(parts) == 2:
                            a, b = float(parts[0].strip()), float(parts[1].strip())
                            result, operation = ris_meta_operator(a, b)
                            self.result_var.set(f"RIS: {result} via {operation}")
                            history_entry = f"[{timestamp}] {expression} = {result} via {operation}"
                        else:
                            self.result_var.set("RIS Error: Format should be @(a,b)")
                            return
                    except Exception:
                        self.result_var.set(f"RIS Error: Cannot parse {expression}")
                        return
                # Try comma-separated values
                elif ',' in expression:
                    parts = expression.replace('(', '').replace(')', '').split(',')
                    if len(parts) == 2:
                        try:
                            a, b = float(parts[0].strip()), float(parts[1].strip())
                            result, operation = ris_meta_operator(a, b)
                            self.result_var.set(f"RIS: {result} via {operation}")
                            history_entry = f"[{timestamp}] RIS({a},{b}) = {result} via {operation}"
                        except Exception:
                            self.result_var.set("RIS Error: Invalid numbers")
                            return
                    else:
                        self.result_var.set("RIS Error: Format should be a,b")
                        return
                else:
                    # Try to intelligently parse arithmetic expressions
                    import re
                    arithmetic_pattern = r'^(\d+(?:\.\d+)?)([+\-*/])(\d+(?:\.\d+)?)$'
                    match = re.match(arithmetic_pattern, expression.replace(' ', ''))
                    if match:
                        a, op, b = match.groups()
                        a, b = float(a), float(b)
                        result, operation = ris_meta_operator(a, b)
                        self.result_var.set(f"RIS: {result} via {operation} (parsed {a}{op}{b})")
                        history_entry = f"[{timestamp}] RIS({a},{b}) = {result} via {operation}"
                    else:
                        self.result_var.set("RIS Error: Use format a,b or simple arithmetic")
                        return
            else:
                # Standard mode with extended operators
                try:
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
                    elif expression.startswith('&[') and expression.endswith(']'):
                        # GCD: &[a,b]
                        parts = expression[2:-1].split(',')
                        if len(parts) == 2:
                            a, b = int(parts[0]), int(parts[1])
                            result = gcd(a, b)
                            self.result_var.set(f"GCD({a},{b}) = {result}")
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
                    else:
                        # Try standard evaluation first
                        try:
                            result = eval(expression)
                            self.result_var.set(str(result))
                            history_entry = f"[{timestamp}] {expression} = {result}"
                        except:
                            # Fall back to UML parsing
                            parsed = parse_uml(expression)
                            result = eval_uml(parsed)
                            self.result_var.set(str(result))
                            history_entry = f"[{timestamp}] {expression} = {result}"
                except ValueError as ve:
                    self.result_var.set(f"Error: {str(ve)}")
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
        """Convert current expression to UML format"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
        
        try:
            # Parse and evaluate the expression first
            result = eval(expression)
            
            # Convert numbers in expression to UML format
            import re
            
            # Find all numbers in the expression
            numbers = re.findall(r'\d+(?:\.\d+)?', expression)
            
            if len(numbers) >= 2:
                # Create UML representation
                uml_parts = [f"[{num}]" for num in numbers]
                operators = re.findall(r'[+\-*/]', expression)
                
                if operators:
                    # Build UML expression
                    uml_expr = f"[{','.join(numbers)}]"
                    self.current_expression.set(uml_expr)
                    self.result_var.set(f"UML: {result}")
                    
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    history_entry = f"[{timestamp}] Converted {expression} → {uml_expr} = {result}"
                    self.history.append(history_entry)
                    self.update_history_display()
                else:
                    self.result_var.set("No operators found to convert")
            else:
                self.result_var.set("Need at least 2 numbers to convert to UML")
                
        except Exception as e:
            self.result_var.set(f"Conversion Error: {str(e)}")
    
    def convert_to_base52(self):
        """Convert current expression to Base52 format"""
        expression = self.current_expression.get().strip()
        if not expression:
            return
        
        try:
            # Parse and evaluate the expression first
            result = eval(expression)
            
            # Convert numbers in expression to Base52
            import re
            
            # Find all numbers in the expression
            numbers = re.findall(r'\d+(?:\.\d+)?', expression)
            
            if numbers:
                # Convert each number to Base52
                base52_numbers = []
                for num_str in numbers:
                    num = int(float(num_str))  # Convert to int for Base52
                    if num > 0:
                        base52_num = base52_encode(num)
                        base52_numbers.append(base52_num)
                    else:
                        base52_numbers.append(str(num))
                
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
            
            # Try standard evaluation first
            try:
                result = eval(expression)
                steps.append(f"Standard evaluation: {result}")
            except:
                steps.append("Standard evaluation failed")
            
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
            "7*7", "9-5", "20/4", "3*3*3"
        ]
        
        results = []
        results.append("=== ARITHMETIC TEST SUITE ===\n")
        
        for expr in test_cases:
            results.append(f"Testing: {expr}")
            
            # Standard mode
            try:
                std_result = eval(expr)
                results.append(f"  Standard: {std_result}")
            except Exception as e:
                results.append(f"  Standard: Error - {e}")
            
            # UML mode
            try:
                uml_result = eval_recursive_compress(expr)
                results.append(f"  UML: {uml_result}")
            except Exception as e:
                results.append(f"  UML: Error - {e}")
            
            # RIS mode (for 2-number expressions)
            import re
            match = re.match(r'^(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)$', expr)
            if match:
                try:
                    a, op, b = match.groups()
                    a, b = float(a), float(b)
                    ris_result, operation = ris_meta_operator(a, b)
                    results.append(f"  RIS: {ris_result} via {operation}")
                except Exception as e:
                    results.append(f"  RIS: Error - {e}")
            else:
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
                std_result = eval(expr)
                results.append(f"  Standard: {std_result}")
                
                uml_result = eval_recursive_compress(expr)
                results.append(f"  UML: {uml_result}")
                
                ris_result, operation = ris_meta_operator(float(a), float(b))
                results.append(f"  RIS: {ris_result} via {operation}")
                
                # Base52 conversion
                base52_a = base52_encode(a)
                base52_b = base52_encode(b)
                base52_result = base52_encode(int(std_result)) if isinstance(std_result, (int, float)) and std_result > 0 else str(std_result)
                results.append(f"  Base52: [{base52_a},{base52_b}] = {base52_result}")
                
            except Exception as e:
                results.append(f"  Error: {e}")
            
            results.append("")  # Empty line        # Show results
        self.show_text_window("Random Test Results", "\n".join(results))
    
    def show_demo(self):
        """Show demo information"""
        messagebox.showinfo("Demo", "Demo feature coming soon!")
    
    def run_tests(self):
        """Run the test suite"""
        messagebox.showinfo("Tests", "Test suite coming soon!")
    
    def show_vector_demo(self):
        messagebox.showinfo("Vector Ops", "Vector operations demo coming soon!")
    def show_matrix_demo(self):
        messagebox.showinfo("Matrix Ops", "Matrix operations demo coming soon!")
    def show_stats_demo(self):
        messagebox.showinfo("Statistics", "Statistics demo coming soon!")
    def show_number_theory_demo(self):
        messagebox.showinfo("Number Theory", "Number theory demo coming soon!")
    def show_base52_demo(self):
        messagebox.showinfo("Base52", "Base52 demo coming soon!")
    def show_si_demo(self):
        messagebox.showinfo("SI Prefixes", "SI prefixes demo coming soon!")
    def ris_demo(self):
        messagebox.showinfo("RIS Meta-Op", "RIS meta-operator demo coming soon!")
    def magic_square_demo(self):
        messagebox.showinfo("Magic Square", "Magic square demo coming soon!")
    def show_fibonacci_demo(self):
        messagebox.showinfo("Fibonacci", "Fibonacci demo coming soon!")
    def show_prime_demo(self):
        messagebox.showinfo("Prime Check", "Prime check demo coming soon!")
    def compression_demo(self):
        messagebox.showinfo("Recursive Compress", "Recursive compression demo coming soon!")
    def show_help(self):
        messagebox.showinfo("Help", "Help coming soon!")
    
    def show_text_window(self, title, text):
        """Show a text in a new window"""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("600x400")
        txt = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Consolas", 10))
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, text)
        txt.config(state=tk.DISABLED)
    
def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python uml_calculator.py [gui|test <expr>]")
        print("  gui  - Launch desktop calculator GUI")
        print("  test <expr> - Evaluate an expression in all modes")
        return
    mode = sys.argv[1].lower()
    if mode == "gui":
        app = UMLCalculatorGUI()
        app.root.mainloop()
    elif mode == "test":
        if len(sys.argv) < 3:
            print("Usage: python uml_calculator.py test <expr>")
            return
        expr = sys.argv[2]
        print(f"Standard: {expr} = {eval(expr)}")
        try:
            parsed = parse_uml(expr)
            print(f"UML: {expr} = {eval_uml(parsed)}")
        except Exception as e:
            print(f"UML: {expr} = Error: {e}")
        try:
            import re
            match = re.match(r'^(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)$', expr)
            if match:
                a, op, b = match.groups()
                a, b = float(a), float(b)
                ris_result, operation = ris_meta_operator(a, b)
                print(f"RIS: {expr} = {ris_result} via {operation}")
            else:
                print("RIS: Not applicable")
        except Exception as e:
            print(f"RIS: {expr} = Error: {e}")
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python uml_calculator.py [gui|test <expr>]")

if __name__ == "__main__":
    main()