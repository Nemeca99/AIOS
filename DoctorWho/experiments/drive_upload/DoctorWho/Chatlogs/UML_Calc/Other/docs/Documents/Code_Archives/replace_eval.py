"""
Script to replace eval() with safe_eval() in uml_calculator.py
"""
import re
import os

def replace_eval_with_safe_eval(file_path):
    print(f"Processing file: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace eval(expression) with safe_eval(expression) but avoid replacing inside comments
    pattern = r'(?<!#.*)eval\(([\w\d_\.\(\)\[\]\{\}\s\'\"]+)\)'
    new_content = re.sub(pattern, r'safe_eval(\1)', content)
    
    if new_content != content:
        print("Found and replaced eval() calls")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print("File updated successfully!")
    else:
        print("No eval() calls found or pattern didn't match")

if __name__ == "__main__":
    calculator_path = r"d:\UML Calculator\UML_Core\uml_calculator.py"
    replace_eval_with_safe_eval(calculator_path)
