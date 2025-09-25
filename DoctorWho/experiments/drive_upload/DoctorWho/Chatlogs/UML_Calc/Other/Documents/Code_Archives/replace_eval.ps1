# PowerShell script to replace eval with safe_eval in the uml_calculator.py file
$file = "d:\UML Calculator\UML_Core\uml_calculator.py"
$content = Get-Content $file -Raw

$content = $content -replace "result = eval\(expression\)", "result = safe_eval(expression)"
$content = $content -replace "std_result = eval\(expr\)", "std_result = safe_eval(expr)"
$content = $content -replace "print\(f`"Standard: \{expr\} = \{eval\(expr\)\}`"\)", "print(f`"Standard: {expr} = {safe_eval(expr)}`")" 

Set-Content $file $content

Write-Host "Replacement completed"
