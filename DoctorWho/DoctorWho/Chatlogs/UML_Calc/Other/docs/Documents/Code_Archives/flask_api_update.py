# Update d:\UML Calculator\UML_Core\uml_calculator.py to add the new API endpoints

'''
Add these Flask API endpoints:
'''

@app.route('/api/convert', methods=['POST'])
def api_convert():
    data = request.json or {}
    expr = data.get('expr', '').strip()
    convert_to = data.get('convert_to', 'uml')
    
    try:
        # Parse and evaluate the expression first
        std_result = eval(expr)
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        
        if convert_to == 'uml':
            # Convert numbers in expression to UML format
            import re
            numbers = re.findall(r'\d+(?:\.\d+)?', expr)
            if len(numbers) >= 2:
                # Create UML representation
                uml_expr = f"[{','.join(numbers)}]"
                result_text = f"UML: {std_result}"
                history_entry = f"[{timestamp}] Converted {expr} → {uml_expr} = {std_result}"
                history.append(history_entry)
                return jsonify({'result': result_text, 'converted': uml_expr, 'history': history[-10:]})
            else:
                return jsonify({'error': 'Need at least 2 numbers to convert to UML'})
        
        elif convert_to == 'base52':
            # Convert numbers in expression to Base52
            import re
            numbers = re.findall(r'\d+(?:\.\d+)?', expr)
            if numbers:
                # Convert each number to Base52
                base52_numbers = []
                for num_str in numbers:
                    num = int(float(num_str))
                    if num > 0:
                        base52_num = base52_encode(num)
                        base52_numbers.append(base52_num)
                    else:
                        base52_numbers.append(str(num))
                
                # Convert result to Base52 too
                result_int = int(std_result) if isinstance(std_result, (int, float)) and std_result > 0 else std_result
                result_base52 = base52_encode(result_int) if isinstance(result_int, int) and result_int > 0 else str(std_result)
                
                if len(base52_numbers) >= 2:
                    base52_expr = f"[{','.join(base52_numbers)}]"
                    result_text = f"Base52: {result_base52}"
                    history_entry = f"[{timestamp}] Base52: {expr} → {base52_expr} = {result_base52}"
                    history.append(history_entry)
                    return jsonify({'result': result_text, 'converted': base52_expr, 'history': history[-10:]})
                else:
                    return jsonify({'error': 'Need at least 2 numbers for Base52 conversion'})
            else:
                return jsonify({'error': 'No numbers found to convert to Base52'})
        
        else:
            return jsonify({'error': f'Unknown conversion type: {convert_to}'})
            
    except Exception as e:
        return jsonify({'error': f'Conversion Error: {str(e)}'})

@app.route('/api/test-suite', methods=['POST'])
def api_test_suite():
    # Run the arithmetic test suite and return results as JSON
    test_cases = [
        "7+7", "1+1", "2*3", "10-4", "15/3",
        "2+3*4", "(5+3)*2", "100/10+5"
    ]
    
    results = {}
    
    for expr in test_cases:
        case_results = {}
        
        # Standard mode
        try:
            std_result = eval(expr)
            case_results["standard"] = {"result": std_result, "status": "success"}
        except Exception as e:
            case_results["standard"] = {"error": str(e), "status": "error"}
        
        # UML mode
        try:
            uml_result = eval_recursive_compress(expr)
            case_results["uml"] = {"result": uml_result, "status": "success"}
        except Exception as e:
            case_results["uml"] = {"error": str(e), "status": "error"}
        
        # Base52 conversion (where possible)
        try:
            std_result = eval(expr)
            if isinstance(std_result, (int, float)) and std_result > 0:
                base52_result = base52_encode(int(std_result))
                case_results["base52"] = {"result": base52_result, "status": "success"}
            else:
                case_results["base52"] = {"result": str(std_result), "status": "success"}
        except Exception as e:
            case_results["base52"] = {"error": str(e), "status": "error"}
        
        results[expr] = case_results
    
    return jsonify({'results': results})

# Update HTML template with conversion buttons
HTML_TEMPLATE = HTML_TEMPLATE.replace("<!-- BUTTONS_PLACEHOLDER -->",
    """<div class="conversion-controls mt-3">
        <div class="row">
            <div class="col">
                <button class="btn btn-info btn-sm w-100" onclick="convertExpression('uml')">Convert to UML</button>
            </div>
            <div class="col">
                <button class="btn btn-warning btn-sm w-100" onclick="convertExpression('base52')">Convert to Base52</button>
            </div>
            <div class="col">
                <button class="btn btn-secondary btn-sm w-100" onclick="runTestSuite()">Run Tests</button>
            </div>
        </div>
    </div>
    <!-- BUTTONS_PLACEHOLDER -->""")

# Update HTML template with conversion functions
HTML_TEMPLATE = HTML_TEMPLATE.replace("// SCRIPTS_PLACEHOLDER",
    """function convertExpression(type) {
        const expr = document.getElementById('expression').value;
        if (!expr) return;
        
        fetch('/api/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expr: expr, convert_to: type })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                displayResult(data.error);
            } else {
                document.getElementById('expression').value = data.converted;
                displayResult(data.result);
                updateHistory(data.history);
            }
        })
        .catch(error => {
            displayResult('Conversion error: ' + error);
        });
    }
    
    function runTestSuite() {
        displayResult('Running test suite...');
        
        fetch('/api/test-suite', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
        .then(response => response.json())
        .then(data => {
            const resultsModal = new bootstrap.Modal(document.getElementById('resultsModal'));
            
            let tableHtml = '<table class="table table-striped"><thead><tr><th>Expression</th><th>Standard</th><th>UML</th><th>Base52</th></tr></thead><tbody>';
            
            for (const [expr, results] of Object.entries(data.results)) {
                tableHtml += `<tr><td>${expr}</td>`;
                
                // Standard column
                if (results.standard.status === 'success') {
                    tableHtml += `<td class="text-success">${results.standard.result}</td>`;
                } else {
                    tableHtml += `<td class="text-danger">${results.standard.error || 'Error'}</td>`;
                }
                
                // UML column
                if (results.uml.status === 'success') {
                    tableHtml += `<td class="text-success">${results.uml.result}</td>`;
                } else {
                    tableHtml += `<td class="text-danger">${results.uml.error || 'Error'}</td>`;
                }
                
                // Base52 column
                if (results.base52.status === 'success') {
                    tableHtml += `<td class="text-success">${results.base52.result}</td>`;
                } else {
                    tableHtml += `<td class="text-danger">${results.base52.error || 'Error'}</td>`;
                }
                
                tableHtml += '</tr>';
            }
            
            tableHtml += '</tbody></table>';
            
            document.getElementById('resultsModalBody').innerHTML = tableHtml;
            resultsModal.show();
        })
        .catch(error => {
            displayResult('Test suite error: ' + error);
        });
    }
    // SCRIPTS_PLACEHOLDER""")

# Add modal for test results
HTML_TEMPLATE = HTML_TEMPLATE.replace("<!-- MODALS_PLACEHOLDER -->",
    """<div class="modal fade" id="resultsModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-scrollable modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Test Suite Results</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="resultsModalBody">
                    <!-- Results will be inserted here -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <!-- MODALS_PLACEHOLDER -->""")
