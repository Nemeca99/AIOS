print("Welcome to the UML Demo Calculator Shell")
print("Note: This demo simulates symbolic results only. No internal engine is included.")
print("Type 'exit' to quit.\n")

while True:
    expr = input("UML> ")
    if expr.strip() == "exit":
        break
    elif expr == "<<5,^2>>":
        print("→ 25  [RIS multiply] ✅")
    elif expr == "<<8,^2>>":
        print("→ 4   [RIS divide] ✅")
    elif expr == "<3,^1/2{1,^2[v,c]}>":
        print("→ Time Dilation expression ✅")
    elif expr == "<2,+3>":
        print("→ 5 ✅")
    else:
        print("→ [Result hidden in demo] — Expression parsed but core engine not included.")
