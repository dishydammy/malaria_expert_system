"""
test_cases.py
-------------
Quick validation script: runs a set of hand-labeled example cases through
the inference engine and reports how many match the expected classification
band. Use the output of this script directly in your report's
"Testing & Validation" section.

Run: python3 test_cases.py
"""

from inference_engine import infer

# Each case: (description, symptom set, expected level)
CASES = [
    ("Classic malaria presentation",
     {"fever", "chills", "sweating", "recent_travel"}, "high"),

    ("Fever + chills only",
     {"fever", "chills"}, "high"),

    ("Fever with vulnerable group (child)",
     {"fever", "vulnerable_group"}, "high"),

    ("Fever + headache + vomiting (overlaps w/ typhoid)",
     {"fever", "headache", "vomiting"}, "high"),

    ("No symptoms reported",
     set(), "low"),

    ("Single weak symptom (fatigue only)",
     {"fatigue"}, "low"),

    ("Headache + fatigue only",
     {"headache", "fatigue"}, "moderate"),

    ("Full symptom set + all risk factors",
     {"fever", "chills", "sweating", "headache", "vomiting", "fatigue",
      "joint_pain", "loss_of_appetite", "recent_travel",
      "mosquito_exposure", "prior_malaria", "vulnerable_group"}, "high"),

    ("Travel history with no symptoms yet",
     {"recent_travel"}, "low"),

    ("Mosquito exposure + joint pain only",
     {"mosquito_exposure", "joint_pain"}, "moderate"),  # borderline case, right at threshold

    ("Chills + sweating, no fever",
     {"chills", "sweating"}, "moderate"),
]


def run():
    correct = 0
    print(f"{'Case':50} {'CF%':>6} {'Got':10} {'Expected':10} {'Match'}")
    print("-" * 90)
    for desc, symptoms, expected in CASES:
        result = infer(symptoms)
        got = result["level"]
        match = "✓" if got == expected else "✗"
        if got == expected:
            correct += 1
        print(f"{desc[:50]:50} {result['cf_percent']:>5.1f}% {got:10} {expected:10} {match}")

    print("-" * 90)
    print(f"Accuracy: {correct}/{len(CASES)} ({100*correct/len(CASES):.1f}%)")


if __name__ == "__main__":
    run()
