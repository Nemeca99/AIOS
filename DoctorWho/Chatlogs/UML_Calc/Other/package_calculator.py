"""
UML Calculator Packaging Script

This script packages the UML Calculator for different deployment targets:
1. CLI (Command Line Interface)
2. Web (Flask-based web application)
3. Android APK (via Kivy, requires additional setup)

It also creates help screens and documentation for each deployment target.
"""

import os
import sys
import shutil
import zipfile
import datetime
import argparse
import subprocess

# Define paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UML_CORE_DIR = os.path.join(ROOT_DIR, 'UML_Core')
DIST_DIR = os.path.join(ROOT_DIR, 'dist')
DOCS_DIR = os.path.join(ROOT_DIR, 'Docs')

# Define package versions
VERSION = '1.0.0'
RELEASE_DATE = datetime.datetime.now().strftime('%Y-%m-%d')

def ensure_directory(directory):
    """Ensure the directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def copy_core_files(target_dir):
    """Copy core UML files to the target directory"""
    core_files = [
        'uml_core.py',
        'uml_calculator.py',
        'safe_eval.py',
        'symbolic_engine.py',
        'symbolic_extensions.py',
        'symbolic_identity.py',
        'magic_dimension.py'
    ]
    
    for file in core_files:
        src = os.path.join(UML_CORE_DIR, file)
        if os.path.exists(src):
            shutil.copy2(src, target_dir)
        else:
            print(f"Warning: File {file} not found, skipping...")

def copy_doc_files(target_dir):
    """Copy documentation files to the target directory"""
    ensure_directory(target_dir)
    
    # Core documentation
    shutil.copy2(os.path.join(ROOT_DIR, 'UML_Calculator_User_Guide.md'), target_dir)
    shutil.copy2(os.path.join(ROOT_DIR, 'UML_Calculator_Quick_Reference.md'), target_dir)
    
    # Copy UML Codex (trimmed version)
    create_trimmed_codex(os.path.join(ROOT_DIR, 'UML_Codex_Complete.md'),
                         os.path.join(target_dir, 'UML_Codex.md'))

def create_trimmed_codex(source, destination):
    """Create a trimmed version of the UML Codex for inclusion in packages"""
    with open(source, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the most important sections (first 30% of content)
    max_length = int(len(content) * 0.3)
    trimmed_content = content[:max_length] + "\n\n...\n\n[Full Codex available in the complete package]"
    
    with open(destination, 'w', encoding='utf-8') as f:
        f.write(trimmed_content)

def create_cli_package():
    """Create CLI package"""
    print("Creating CLI package...")
    target_dir = os.path.join(DIST_DIR, 'uml_calculator_cli')
    ensure_directory(target_dir)
    
    # Copy core files
    copy_core_files(target_dir)
    
    # Create CLI launcher
    with open(os.path.join(target_dir, 'uml_calculator_cli.py'), 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
UML Calculator CLI
Command line interface for the Universal Mathematical Language Calculator
\"\"\"

import sys
import os
import argparse

# Import UML core components
from uml_core import parse_uml, eval_uml, convert_standard_to_uml
from uml_calculator import UMLCalculatorCLI
from safe_eval import safe_eval

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='UML Calculator Command Line Interface')
    parser.add_argument('expression', nargs='?', help='Expression to evaluate')
    parser.add_argument('-u', '--uml', action='store_true', help='Parse as UML expression')
    parser.add_argument('-c', '--convert', action='store_true', help='Convert standard expression to UML')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('-v', '--version', action='store_true', help='Show version info')
    args = parser.parse_args()
    
    # Show version
    if args.version:
        print(f"UML Calculator CLI v{VERSION}")
        print(f"Release Date: {RELEASE_DATE}")
        return
    
    # Interactive mode
    if args.interactive or not args.expression:
        calculator = UMLCalculatorCLI()
        calculator.run()
        return
    
    # Single expression mode
    try:
        if args.convert:
            uml_expr = convert_standard_to_uml(args.expression)
            print(f"UML: {uml_expr}")
            
        if args.uml:
            parsed = parse_uml(args.expression)
            result = eval_uml(parsed)
        else:
            # Try as standard expression first, fall back to UML
            try:
                result = safe_eval(args.expression)
            except:
                parsed = parse_uml(args.expression)
                result = eval_uml(parsed)
        
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
""".replace("VERSION", VERSION).replace("RELEASE_DATE", RELEASE_DATE))
    
    # Create documentation
    doc_dir = os.path.join(target_dir, 'docs')
    copy_doc_files(doc_dir)
    
    # Create README
    with open(os.path.join(target_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f"""# UML Calculator CLI

Universal Mathematical Language Calculator - Command Line Interface

Version: {VERSION}
Release Date: {RELEASE_DATE}

## Usage

```
python uml_calculator_cli.py [expression] [-u] [-c] [-i] [-v]
```

Options:
- `-u`, `--uml`: Parse expression as UML syntax
- `-c`, `--convert`: Convert standard math notation to UML
- `-i`, `--interactive`: Run in interactive mode
- `-v`, `--version`: Show version info

## Examples

```
# Standard notation
python uml_calculator_cli.py "3 + 4 * 2"

# UML notation
python uml_calculator_cli.py "[3,<4,2>]" -u

# Convert standard to UML
python uml_calculator_cli.py "3 + 4 * 2" -c

# Interactive mode
python uml_calculator_cli.py -i
```

## Documentation

See the `docs` directory for more information:
- UML_Calculator_User_Guide.md
- UML_Calculator_Quick_Reference.md
- UML_Codex.md (shortened version)
""")
    
    # Create ZIP package
    zip_path = os.path.join(DIST_DIR, f'uml_calculator_cli_v{VERSION}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, target_dir)
                zipf.write(file_path, arcname)
    
    print(f"CLI package created: {zip_path}")

def create_web_package():
    """Create web package"""
    print("Creating Web package...")
    target_dir = os.path.join(DIST_DIR, 'uml_calculator_web')
    ensure_directory(target_dir)
    
    # Create directories
    static_dir = os.path.join(target_dir, 'static')
    templates_dir = os.path.join(target_dir, 'templates')
    ensure_directory(static_dir)
    ensure_directory(templates_dir)
    
    # Copy core files
    copy_core_files(target_dir)
    
    # Create web app
    with open(os.path.join(target_dir, 'app.py'), 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
UML Calculator Web Application
Flask-based web interface for the Universal Mathematical Language Calculator
\"\"\"

from flask import Flask, request, render_template, jsonify
import os
import datetime
import sys

# Import UML core components
from uml_core import parse_uml, eval_uml, convert_standard_to_uml, recursive_compress
from safe_eval import safe_eval

app = Flask(__name__)
VERSION = "VERSION"
RELEASE_DATE = "RELEASE_DATE"

# Store calculation history
history = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', version=VERSION, release_date=RELEASE_DATE)

@app.route('/api/calc', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expr = data.get('expression', '')
        mode = data.get('mode', 'auto')  # 'auto', 'standard', or 'uml'
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if not expr:
            return jsonify({'error': 'No expression provided'})
        
        if mode == 'uml' or (mode == 'auto' and expr[0] in '[{<@'):
            # UML mode
            try:
                parsed = parse_uml(expr)
                result_val = eval_uml(parsed)
                result = f"{result_val}"
            except Exception as e:
                return jsonify({'error': f'UML evaluation error: {str(e)}'})
        else:
            # Standard mode
            try:
                result_val = safe_eval(expr)
                result = f"{result_val}"
            except Exception as e:
                try:
                    # Fall back to UML
                    parsed = parse_uml(expr)
                    result_val = eval_uml(parsed)
                    result = f"{result_val}"
                except Exception as e2:
                    return jsonify({'error': f'Evaluation error: {str(e)}. UML fallback error: {str(e2)}'})
        
        # Add to history
        history.append(f"[{timestamp}] {expr} = {result}")
        if len(history) > 100:
            history.pop(0)  # Remove oldest entry if history gets too long
        
        return jsonify({
            'result': result,
            'expression': expr,
            'history': history[-10:],  # Return the 10 most recent entries
        })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'})

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        expr = data.get('expression', '')
        
        if not expr:
            return jsonify({'error': 'No expression provided'})
        
        uml_expr = convert_standard_to_uml(expr)
        return jsonify({'uml': uml_expr})
    except Exception as e:
        return jsonify({'error': f'Conversion error: {str(e)}'})

@app.route('/api/evaluate', methods=['POST'])
def safe_evaluate():
    \"\"\"
    Endpoint to safely evaluate mathematical expressions for graphing.
    Replaces client-side eval() with server-side safe_eval.
    \"\"\"
    try:
        data = request.get_json()
        expression = data['expression']
        x_val = data['x']
        
        # Replace x with the actual value in the expression
        expression = expression.replace('x', f'({x_val})')
        
        # Use safe_eval to evaluate the expression
        try:
            result = safe_eval(expression)
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e), 'result': float('nan')}), 400
    except Exception as e:
        return jsonify({'error': str(e), 'result': float('nan')}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
""".replace("VERSION", VERSION).replace("RELEASE_DATE", RELEASE_DATE))
    
    # Create index.html template
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UML Calculator</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container mt-4">
        <h1 class="text-center">Universal Mathematical Language Calculator</h1>
        <h5 class="text-center text-muted">Version {{ version }} | {{ release_date }}</h5>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <ul class="nav nav-tabs card-header-tabs">
                            <li class="nav-item">
                                <a class="nav-link active" id="calculator-tab" href="#">Calculator</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="graph-tab" href="#">Graphing</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="help-tab" href="#">Help</a>
                            </li>
                        </ul>
                    </div>
                    <div class="card-body">
                        <!-- Calculator Panel -->
                        <div id="calculator-panel">
                            <div class="mb-3">
                                <label for="expression" class="form-label">Expression:</label>
                                <div class="input-group">
                                    <input type="text" id="expression" class="form-control" placeholder="Enter expression (e.g., 3 + 4 or [3,4])">
                                    <button class="btn btn-primary" id="calculate-btn">Calculate</button>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" name="mode" id="mode-auto" value="auto" checked>
                                    <label class="form-check-label" for="mode-auto">Auto-detect</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" name="mode" id="mode-standard" value="standard">
                                    <label class="form-check-label" for="mode-standard">Standard Math</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" name="mode" id="mode-uml" value="uml">
                                    <label class="form-check-label" for="mode-uml">UML Syntax</label>
                                </div>
                            </div>
                            <div class="result-box p-3 mb-3" id="result-display">
                                Result will appear here
                            </div>
                            <div class="mb-3">
                                <button class="btn btn-outline-secondary btn-sm" id="convert-btn">Convert to UML</button>
                                <button class="btn btn-outline-secondary btn-sm" id="copy-btn">Copy Result</button>
                                <button class="btn btn-outline-secondary btn-sm" id="clear-btn">Clear</button>
                            </div>
                        </div>
                        
                        <!-- Graphing Panel -->
                        <div id="graph-panel" style="display: none;">
                            <div class="mb-3">
                                <label for="function-input" class="form-label">Function(s):</label>
                                <div class="input-group">
                                    <input type="text" id="function-input" class="form-control" placeholder="Enter function of x (e.g., x^2 + 3x + 1)">
                                    <button class="btn btn-primary" id="graph-btn">Plot</button>
                                </div>
                                <small class="form-text text-muted">Separate multiple functions with semicolons</small>
                            </div>
                            <div class="graph-container" id="graph-container"></div>
                            <div class="mt-2">
                                <button class="btn btn-sm btn-outline-secondary" id="zoom-in">Zoom In</button>
                                <button class="btn btn-sm btn-outline-secondary" id="zoom-out">Zoom Out</button>
                                <button class="btn btn-sm btn-outline-secondary" id="reset-zoom">Reset</button>
                            </div>
                        </div>
                        
                        <!-- Help Panel -->
                        <div id="help-panel" style="display: none;">
                            <h4>Quick Reference</h4>
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Operation</th>
                                        <th>Standard Notation</th>
                                        <th>UML Notation</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Addition</td>
                                        <td>3 + 4</td>
                                        <td>[3,4]</td>
                                    </tr>
                                    <tr>
                                        <td>Subtraction</td>
                                        <td>7 - 2</td>
                                        <td>{7,2}</td>
                                    </tr>
                                    <tr>
                                        <td>Multiplication</td>
                                        <td>6 * 8</td>
                                        <td>&lt;6,8&gt;</td>
                                    </tr>
                                    <tr>
                                        <td>Division</td>
                                        <td>20 / 5</td>
                                        <td>&lt;&gt;20,5&lt;&gt;</td>
                                    </tr>
                                    <tr>
                                        <td>Exponentiation</td>
                                        <td>2 ** 3</td>
                                        <td>@(2,3)</td>
                                    </tr>
                                    <tr>
                                        <td>Complex Expression</td>
                                        <td>(3 + 4) * 2</td>
                                        <td>&lt;[3,4],2&gt;</td>
                                    </tr>
                                </tbody>
                            </table>
                            <p><a href="#" id="full-docs-link">View Full Documentation</a></p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">History</div>
                    <div class="card-body history-panel">
                        <ul id="history-list" class="list-group list-group-flush"></ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap and Plotly JS -->
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/plotly.min.js') }}"></script>
    
    <!-- Calculator Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Tab switching
            const calculatorTab = document.getElementById('calculator-tab');
            const graphTab = document.getElementById('graph-tab');
            const helpTab = document.getElementById('help-tab');
            const calculatorPanel = document.getElementById('calculator-panel');
            const graphPanel = document.getElementById('graph-panel');
            const helpPanel = document.getElementById('help-panel');
            
            calculatorTab.addEventListener('click', function(e) {
                e.preventDefault();
                calculatorPanel.style.display = 'block';
                graphPanel.style.display = 'none';
                helpPanel.style.display = 'none';
                calculatorTab.classList.add('active');
                graphTab.classList.remove('active');
                helpTab.classList.remove('active');
            });
            
            graphTab.addEventListener('click', function(e) {
                e.preventDefault();
                calculatorPanel.style.display = 'none';
                graphPanel.style.display = 'block';
                helpPanel.style.display = 'none';
                calculatorTab.classList.remove('active');
                graphTab.classList.add('active');
                helpTab.classList.remove('active');
            });
            
            helpTab.addEventListener('click', function(e) {
                e.preventDefault();
                calculatorPanel.style.display = 'none';
                graphPanel.style.display = 'none';
                helpPanel.style.display = 'block';
                calculatorTab.classList.remove('active');
                graphTab.classList.remove('active');
                helpTab.classList.add('active');
            });
            
            // Calculator logic
            const expressionInput = document.getElementById('expression');
            const calculateBtn = document.getElementById('calculate-btn');
            const resultDisplay = document.getElementById('result-display');
            const modeAuto = document.getElementById('mode-auto');
            const modeStandard = document.getElementById('mode-standard');
            const modeUml = document.getElementById('mode-uml');
            const convertBtn = document.getElementById('convert-btn');
            const copyBtn = document.getElementById('copy-btn');
            const clearBtn = document.getElementById('clear-btn');
            const historyList = document.getElementById('history-list');
            
            function calculate() {
                const expr = expressionInput.value.trim();
                if (!expr) return;
                
                let mode = 'auto';
                if (modeStandard.checked) mode = 'standard';
                if (modeUml.checked) mode = 'uml';
                
                fetch('/api/calc', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        expression: expr,
                        mode: mode
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultDisplay.innerHTML = `<span class="text-danger">${data.error}</span>`;
                    } else {
                        resultDisplay.textContent = data.result;
                        updateHistory(data.history);
                    }
                })
                .catch(error => {
                    resultDisplay.innerHTML = `<span class="text-danger">Server error: ${error.message}</span>`;
                });
            }
            
            function convertToUml() {
                const expr = expressionInput.value.trim();
                if (!expr) return;
                
                fetch('/api/convert', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        expression: expr
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        resultDisplay.innerHTML = `<span class="text-danger">${data.error}</span>`;
                    } else {
                        expressionInput.value = data.uml;
                        modeUml.checked = true;
                    }
                })
                .catch(error => {
                    resultDisplay.innerHTML = `<span class="text-danger">Server error: ${error.message}</span>`;
                });
            }
            
            function updateHistory(history) {
                historyList.innerHTML = '';
                history.forEach(item => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item';
                    li.textContent = item;
                    historyList.appendChild(li);
                });
            }
            
            calculateBtn.addEventListener('click', calculate);
            expressionInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') calculate();
            });
            
            convertBtn.addEventListener('click', convertToUml);
            
            copyBtn.addEventListener('click', function() {
                const result = resultDisplay.textContent;
                navigator.clipboard.writeText(result)
                    .then(() => {
                        const originalText = copyBtn.textContent;
                        copyBtn.textContent = 'Copied!';
                        setTimeout(() => { copyBtn.textContent = originalText; }, 1000);
                    });
            });
            
            clearBtn.addEventListener('click', function() {
                expressionInput.value = '';
                resultDisplay.textContent = 'Result will appear here';
                expressionInput.focus();
            });
            
            // Graphing logic
            let graphLayout = {
                margin: {t:30, b:40, l:50, r:20}, 
                title: 'y = f(x)', 
                xaxis: {title: 'x', range: [-10, 10]}, 
                yaxis: {title: 'y', autorange: true}
            };
            
            Plotly.newPlot('graph-container', [], graphLayout, {responsive: true});
            
            document.getElementById('graph-btn').addEventListener('click', function() {
                const funcStr = document.getElementById('function-input').value.trim();
                if (!funcStr) return;
                
                const funcs = funcStr.split(';').map(f => f.trim()).filter(f => f);
                const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                                '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'];
                
                let graphData = [];
                
                funcs.forEach((func, idx) => {
                    // Call the server to evaluate the function at various points
                    const x = [], y = [];
                    for (let i = graphLayout.xaxis.range[0]; i <= graphLayout.xaxis.range[1]; i += 0.2) {
                        x.push(i);
                        
                        // Call the API for each point (this is inefficient but safer)
                        fetch('/api/evaluate', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({expression: func, x: i})
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (!isNaN(data.result)) {
                                y.push(data.result);
                                if (y.length === x.length) {
                                    // When we have all the points, update the graph
                                    graphData.push({
                                        x: x,
                                        y: y,
                                        mode: 'lines',
                                        line: {color: colors[idx % colors.length]},
                                        name: func
                                    });
                                    
                                    if (graphData.length === funcs.length) {
                                        Plotly.newPlot('graph-container', graphData, graphLayout);
                                    }
                                }
                            }
                        })
                        .catch(error => console.error('Error evaluating function:', error));
                    }
                });
            });
            
            document.getElementById('zoom-in').addEventListener('click', function() {
                const range = graphLayout.xaxis.range;
                const center = (range[0] + range[1]) / 2;
                const width = (range[1] - range[0]) * 0.7;
                graphLayout.xaxis.range = [center - width/2, center + width/2];
                Plotly.relayout('graph-container', {'xaxis.range': graphLayout.xaxis.range});
            });
            
            document.getElementById('zoom-out').addEventListener('click', function() {
                const range = graphLayout.xaxis.range;
                const center = (range[0] + range[1]) / 2;
                const width = (range[1] - range[0]) * 1.5;
                graphLayout.xaxis.range = [center - width/2, center + width/2];
                Plotly.relayout('graph-container', {'xaxis.range': graphLayout.xaxis.range});
            });
            
            document.getElementById('reset-zoom').addEventListener('click', function() {
                graphLayout.xaxis.range = [-10, 10];
                Plotly.relayout('graph-container', {'xaxis.range': graphLayout.xaxis.range});
            });
            
            // Help panel
            document.getElementById('full-docs-link').addEventListener('click', function(e) {
                e.preventDefault();
                window.open('/static/docs/UML_Calculator_User_Guide.md');
            });
        });
    </script>
</body>
</html>""")
    
    # Create CSS
    ensure_directory(os.path.join(static_dir, 'css'))
    with open(os.path.join(static_dir, 'css', 'style.css'), 'w', encoding='utf-8') as f:
        f.write("""body {
    background-color: #f5f5f5;
}

.result-box {
    background-color: #e9ecef;
    border-radius: 4px;
    min-height: 50px;
    font-family: monospace;
    font-size: 1.2em;
    word-break: break-word;
}

.history-panel {
    max-height: 400px;
    overflow-y: auto;
}

.graph-container {
    height: 400px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

#history-list .list-group-item {
    font-family: monospace;
    font-size: 0.9em;
    padding: 0.5rem 0.75rem;
}
""")
    
    # Create docs directory in static
    docs_dir = os.path.join(static_dir, 'docs')
    copy_doc_files(docs_dir)
    
    # Create requirements.txt
    with open(os.path.join(target_dir, 'requirements.txt'), 'w', encoding='utf-8') as f:
        f.write("""flask>=2.0.0
numpy>=1.20.0
gunicorn>=20.1.0  # For production deployment
""")
    
    # Create README
    with open(os.path.join(target_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f"""# UML Calculator Web Application

Universal Mathematical Language Calculator - Web Interface

Version: {VERSION}
Release Date: {RELEASE_DATE}

## Setup

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and navigate to http://localhost:5000

## Features

- Standard and UML notation support
- Auto-detection of syntax
- Conversion between notations
- Function graphing
- Calculation history
- Reference documentation

## Deployment

For production deployment:

```
gunicorn app:app
```

## Documentation

See the `static/docs` directory for more information:
- UML_Calculator_User_Guide.md
- UML_Calculator_Quick_Reference.md
- UML_Codex.md (shortened version)
""")
    
    # Create ZIP package
    zip_path = os.path.join(DIST_DIR, f'uml_calculator_web_v{VERSION}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, target_dir)
                zipf.write(file_path, arcname)
    
    print(f"Web package created: {zip_path}")

def main():
    """Main packaging function"""
    parser = argparse.ArgumentParser(description='UML Calculator Packaging Script')
    parser.add_argument('--all', action='store_true', help='Create all packages')
    parser.add_argument('--cli', action='store_true', help='Create CLI package')
    parser.add_argument('--web', action='store_true', help='Create Web package')
    args = parser.parse_args()
    
    # Create distribution directory if it doesn't exist
    ensure_directory(DIST_DIR)
    
    # Create packages based on arguments
    if args.all or args.cli:
        create_cli_package()
    
    if args.all or args.web:
        create_web_package()
    
    if not (args.all or args.cli or args.web):
        # Default to creating all packages if no arguments provided
        create_cli_package()
        create_web_package()
    
    print("Packaging complete!")

if __name__ == '__main__':
    main()
