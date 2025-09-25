# UML Conversion Guide

UML (Universal Mathematical Language) replaces classical symbols with nested, shape-based bracket structures. Each bracket has meaning and resolves from deepest outward.

---

## 🔢 Bracket Operators

| UML Symbol | Meaning        | Classical Equivalent |
|------------|----------------|-----------------------|
| `<a,+b>`   | Addition        | a + b                |
| `<a,-b>`   | Subtraction     | a - b                |
| `<a,^b>`   | Multiplication  | a * b                |
| `<a,/b>`   | Division        | a / b                |
| `<<a,^b>>` | RIS Meta-Op     | See RIS rules below  |

---

## 🔁 RIS Logic

RIS(a, b):

- If a > 1 and b > 1: → multiplication
- If a > b and a % b == 0: → division
- If a == b: → exponentiation
- If either a or b == 0: → return 0
- Default: → addition

---

## 📘 Examples

### Standard: `5 * 3 = 15`  
UML: `<5,^3>` → 15

### RIS: `RIS(5,2)`  
UML: `<<5,^2>>` → 25

### Einstein Time Dilation:  
Classical: `t' = t / sqrt(1 - v² / c²)`  
UML: `<t,^½{1,^2[v,c]}>`
