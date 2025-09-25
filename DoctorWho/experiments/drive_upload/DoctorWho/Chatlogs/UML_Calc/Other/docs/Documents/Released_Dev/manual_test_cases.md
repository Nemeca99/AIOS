🧪 UML Calculator Manual Test Cases
✅ 1. Standard Arithmetic (Baseline Validation)
Input	Expected Output	Notes
2 + 2	4	Basic addition
6 * 3	18	Basic multiplication
10 - 4	6	Subtraction
8 / 2	4	Division
2^3	8	Exponentiation
✅ 2. RIS Meta-Operator Logic
Input	Expected Output	Notes
RIS(6,3)	18	Prioritize multiplication for a > 1, b > 1
RIS(8,2)	4	Prioritize division when a > b and a % b == 0
RIS(5,1)	6	Addition as fallback when b = 1
RIS(1,1)	1	Identity case
RIS(RIS(5,5), RIS(2,8))	100	Nested RIS collapse test (with correct compression behavior)
✅ 3. UML Expression Parsing
Input (UML)	Expected Output	Notes
<2,+3>	5	UML addition notation
<2,^3>	8	UML exponentiation
<4,^½>	2	UML square root (via exponent 1/2)
<t,^½{1,^2[v,c]}>	Relativity Format	UML representation of time dilation
✅ 4. Base52 Encoding (Language Compression)
Input	Expected Output	Notes
base52_encode(27)	'a'	Lowercase mapping
base52_encode(1)	'A'	Uppercase mapping
base52_encode(0)	Error or Guard	Edge case protection
✅ 5. Symbolic Encoding (Word Arrays)
Input (Lang Mode)	Expected Output	Notes
[8,5,12,12,15,0~23,15,18,12,4]	'HELLO WORLD'	Capital encoding + spacing
[8,5,12,12,15,0~23,15,18,12,4,!]	'HELLO WORLD!'	Grammar character support
[1,2,3,:,4,5]	'ABC:DE'	Punctuation supported in Lang mode
✅ 6. Recursive Compression
Input	Expected Output	Notes
recursive_compress([2,2])	4	Handles multiplicative compression
recursive_compress([RIS(4,2), RIS(2,2)])	16	RIS nesting with compression logic
✅ 7. Error Handling & Resilience
Input	Expected Result	Notes
2 / 0	Error: Division by zero	Catch critical math error
base52_encode(-1)	Error: Invalid input	Negative base52 encoding should fail
eval('bad_code')	Secure failure	No eval allowed — safe_eval used
🧩 Optional: Showcase Tests
🔷 Magic Square / Perfect Square Identity

    If included: use a nested <RIS> matrix pattern to produce a magic square where the sum of rows, columns, diagonals are equal.