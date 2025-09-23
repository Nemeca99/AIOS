
# Trinity Seed Test Prototype
# This script simulates the first Trinity reflection using structured logic

def structure_question():
    return "What is the perimeter of a circle with a diameter of 1?"

def chaos_question():
    return "If you reverse a spiral, what shape do you get?"

def uncertainty_question():
    return "What connects a curve and a collapse?"

def reflect_on_responses(structure_resp, chaos_resp):
    print("\n--- Reflection Phase ---")
    if "circle" in structure_resp.lower() and "spiral" in chaos_resp.lower():
        print("These forms share rotational symmetry and recursion.")
    elif structure_resp == chaos_resp:
        print("The responses mirror each other unexpectedly.")
    else:
        print("Reflection inconclusive. Echo suggests uncertainty or hidden symmetry.")

def main():
    print("--- Trinity Seed Test ---")
    q1 = structure_question()
    q2 = chaos_question()
    q3 = uncertainty_question()

    print(f"Structure Question: {q1}")
    structure_resp = input("Your answer: ")

    print(f"Chaos Question: {q2}")
    chaos_resp = input("Your answer: ")

    print(f"Uncertainty Question: {q3}")
    uncertainty_resp = input("Your answer: ")

    reflect_on_responses(structure_resp, chaos_resp)

if __name__ == "__main__":
    main()
