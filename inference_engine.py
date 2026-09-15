"""
inference_engine.py
--------------------
The reasoning core of the expert system.

Takes the set of symptoms/risk factors a user has selected ("working
memory" of facts) and applies the rules from knowledge_base.py using
the standard Certainty Factor (CF) combination formula:

    CF_combined = CF1 + CF2 * (1 - CF1)

This formula is the classic MYCIN-style method for combining independent
pieces of positive evidence: each additional confirming rule increases
confidence, but with diminishing returns as CF approaches 1.0.
"""

from knowledge_base import ALL_RULES, classify


def infer(selected_symptoms: set):
    """
    selected_symptoms: a set of symptom ids the user answered 'yes' to.

    Returns a dict with:
        - cf: final combined certainty factor (0.0 - 1.0)
        - label: classification label
        - advice: recommended next step
        - fired_rules: list of rules that matched, each with its own CF,
          for the explanation facility
    """
    combined_cf = 0.0
    fired_rules = []

    for rule in ALL_RULES:
        conditions = rule["if"]
        if all(cond in selected_symptoms for cond in conditions):
            rule_cf = rule["cf"]
            fired_rules.append({
                "id": rule["id"],
                "text": rule["text"],
                "cf": rule_cf,
            })
            # Standard CF combination for positive evidence
            combined_cf = combined_cf + rule_cf * (1 - combined_cf)

    combined_cf = round(combined_cf, 3)
    label, advice, level = classify(combined_cf)

    # Sort fired rules by strongest contribution first, for a clearer explanation
    fired_rules.sort(key=lambda r: r["cf"], reverse=True)

    return {
        "cf": combined_cf,
        "cf_percent": round(combined_cf * 100, 1),
        "label": label,
        "advice": advice,
        "level": level,
        "fired_rules": fired_rules,
    }
