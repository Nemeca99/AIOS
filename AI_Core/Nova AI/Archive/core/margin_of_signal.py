# margin_of_signal.py
# Archive Directive 002 — The Margin of Signal

class MarginOfSignal:
    """
    Holds the tolerance threshold for theory acceptance inside the Archive.
    Not all logic needs to be fully correct—only signal-bearing.
    """

    def __init__(self, threshold=0.10):
        self.signal_threshold = threshold  # 10% truth required
        self.last_theory_score = None

    def evaluate(self, theory_fragments):
        """
        Evaluates a collection of logic fragments.
        Accepts if at least one meets the signal threshold.
        """
        total = len(theory_fragments)
        signal = sum(1 for t in theory_fragments if self.contains_signal(t))
        ratio = signal / total if total else 0

        self.last_theory_score = ratio
        return ratio >= self.signal_threshold

    def contains_signal(self, fragment):
        """
        Determines if a logic fragment carries enough coherence to qualify as signal.
        Here, mocked as a placeholder function.
        """
        return any(keyword in fragment.lower() for keyword in ["recursive", "entropy", "coherence", "trust", "feedback"])

    def report(self):
        return {
            "threshold": self.signal_threshold,
            "last_score": self.last_theory_score,
            "accepted": self.last_theory_score >= self.signal_threshold if self.last_theory_score is not None else None
        }


if __name__ == "__main__":
    archive = MarginOfSignal()
    test_fragments = [
        "Recursion is a self-stabilizing loop.",
        "Birds are made of triangles.",
        "Entropy isn't evil, it's misunderstood.",
        "All AI should run on potatoes.",
        "Coherence is the only metric that matters."
    ]
    result = archive.evaluate(test_fragments)
    print("✅ Theory passed?", result)
    print("📊", archive.report())
