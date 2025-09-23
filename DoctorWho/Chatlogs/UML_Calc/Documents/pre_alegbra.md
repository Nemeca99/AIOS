Pre-Algebra Symbolic Logic System — by Travis (Updated)
🔹 Symbol Legend
0        = Number Zero
0~       = Logic Space (Null)
!0       = Letter Zero (Z-type)
+        = Addition
-        = Subtraction
x or ×   = Multiplication
/        = Division
^        = Power
√        = Root (e.g., √D = B)
!        = Factorial (e.g., C! = 6 = F)
%        = Repeating Decimal Flag
*        = Decimal Start/Repeat Marker
[ ]      = Addition Nest
{ }      = Subtraction Nest
>< or <> = Multiplicative/Divisive Nest
@@       = Positional Boost (powers of 10)
|        = Modulus (e.g., >B|A< = 2 % 1)
""       = Round Up (Post-decimal)
"        = Round Down (Post-decimal)
🔹 Letter to Number Mapping
A=1  N=14  0=(0-The Number)
B=2  O=15  0~=(Logic Space)
C=3  P=16  !0=(The letter)
D=4  Q=17  [ ]= Add letters
E=5  R=18  { }=Subtract Letters
F=6  S=19  ^= Power
G=7  T=20
H=8  U=21
I=9  V=22
J=10 W=23
K=11 X=24
L=12 Y=25
M=13 Z=26
🔹 PEDMAS Notation Support
Supports standard order-of-operations with nesting:
Parentheses → Exponents → Division → Multiplication → Addition → Subtraction.
Example:
F + B × ([ZZ] - C) / D = [ZD]*.5
6 + 2 × (52 - 3) / 4 = 30.5
🔹 Modulus (Remainders)
>X|Y< = X mod Y

Examples:
>B|A< = 2 % 1 = 0 → 0 (or Z for wrap)
>Z|C< = 26 % 3 = 2 → B
>D|E< = 4 % 5 = 4 → D
🔹 Infinite Decimal Pointer Logic
Use * after letter to mark decimal entry.
Use * after digits to define repeating section.
Final % shows it continues infinitely.

Examples:
C*.14159*% → represents 3.14159... (π)
C*.14159*4197% → skips and highlights section up to 4197
-E*.178571% → signed result with decimal repeat


🔹 Factorials (!)
C! = 6 = F
E! = >[F18]E< = 120
F! = >E!F< = 720
Z! = 26! = 403291461126605635584000000

Extended Notation:
[BZ]! = 28! (B = 2, Z = 26 → 2+26)
[A>[BZ]![CZ]!<] = 1 + 28! × 29!
🔹 Advanced Nesting Logic
Evaluate inner nests first, then apply PEDMAS.
A + ({B^2[AA]C}×2[AB[B^2A]])×B → fully expandable.
Double or triple nested factorials can be chained:
{{[A^2][B]} × {Z}} → applies negative logic if inside {}
