"""
knowledge_base.py
------------------
Knowledge base for the Malaria Diagnosis Expert System (CSC 520 Group Project).

Encodes clinical knowledge as IF-THEN rules with Certainty Factors (CF).
CF values (0.0 - 1.0) express how strongly a given piece of evidence supports
a malaria diagnosis, based on general clinical literature and WHO / national
malaria guideline patterns (fever, chills, headache, vomiting, fatigue,
myalgia, sweating, travel/exposure history, and vulnerable-group status).

IMPORTANT (state this in your report too):
This is an EDUCATIONAL DECISION-SUPPORT TOOL, not a clinical diagnostic
device. A confirmed malaria diagnosis requires a Rapid Diagnostic Test (RDT)
or microscopy. CF values here are illustrative, derived from general
symptom-prevalence literature, not a validated clinical model.
"""

# -----------------------------------------------------------------------
# 1. FACTS: the symptoms / risk factors the system can ask about
# -----------------------------------------------------------------------
# key: internal id, label: shown to user, group: for UI sectioning
SYMPTOMS = [
    {"id": "fever", "label": "Fever (measured or felt)", "group": "Primary Symptoms"},
    {"id": "chills", "label": "Chills / shivering", "group": "Primary Symptoms"},
    {"id": "sweating", "label": "Excessive sweating", "group": "Primary Symptoms"},
    {"id": "headache", "label": "Headache", "group": "Secondary Symptoms"},
    {"id": "vomiting", "label": "Nausea or vomiting", "group": "Secondary Symptoms"},
    {"id": "fatigue", "label": "Fatigue / general weakness", "group": "Secondary Symptoms"},
    {"id": "joint_pain", "label": "Joint or muscle pain (myalgia)", "group": "Secondary Symptoms"},
    {"id": "loss_of_appetite", "label": "Loss of appetite", "group": "Secondary Symptoms"},
    {"id": "recent_travel", "label": "Recent travel/residence in a malaria-endemic area (last 2-4 weeks)", "group": "Risk Factors"},
    {"id": "mosquito_exposure", "label": "Frequent mosquito bites / no bed net use", "group": "Risk Factors"},
    {"id": "prior_malaria", "label": "Prior history of malaria", "group": "Risk Factors"},
    {"id": "vulnerable_group", "label": "Patient is a child under 5, pregnant, or immunocompromised", "group": "Risk Factors"},
]

# -----------------------------------------------------------------------
# 2. RULES: single-symptom (base) rules
# -----------------------------------------------------------------------
# Each rule fires independently if its symptom is present.
BASE_RULES = [
    {"id": "R1", "if": ["fever"], "cf": 0.55,
     "text": "IF fever THEN suspect malaria (fever is the cardinal symptom of malaria)"},
    {"id": "R2", "if": ["chills"], "cf": 0.45,
     "text": "IF chills THEN suspect malaria (classic paroxysm symptom)"},
    {"id": "R3", "if": ["sweating"], "cf": 0.35,
     "text": "IF profuse sweating THEN suspect malaria (sweating stage of a malaria paroxysm)"},
    {"id": "R4", "if": ["headache"], "cf": 0.25,
     "text": "IF headache THEN weakly suspect malaria (also common to many febrile illnesses)"},
    {"id": "R5", "if": ["vomiting"], "cf": 0.30,
     "text": "IF vomiting/nausea THEN suspect malaria"},
    {"id": "R6", "if": ["fatigue"], "cf": 0.20,
     "text": "IF fatigue THEN weakly suspect malaria"},
    {"id": "R7", "if": ["joint_pain"], "cf": 0.25,
     "text": "IF joint/muscle pain THEN suspect malaria"},
    {"id": "R8", "if": ["loss_of_appetite"], "cf": 0.15,
     "text": "IF loss of appetite THEN weakly suspect malaria"},
    {"id": "R9", "if": ["recent_travel"], "cf": 0.35,
     "text": "IF recent travel to an endemic area THEN raise malaria exposure suspicion "
             "(exposure risk alone, not illness evidence)"},
    {"id": "R10", "if": ["mosquito_exposure"], "cf": 0.20,
     "text": "IF frequent mosquito exposure with no bed net THEN mildly raise "
             "malaria exposure suspicion"},
    {"id": "R11", "if": ["prior_malaria"], "cf": 0.20,
     "text": "IF prior history of malaria THEN mildly raise suspicion (recurrence risk)"},
]

# -----------------------------------------------------------------------
# 3. COMPOUND RULES: symptom combinations that are stronger indicators
#    than any single symptom (these fire IN ADDITION to base rules)
# -----------------------------------------------------------------------
COMPOUND_RULES = [
    {"id": "C1", "if": ["fever", "chills", "sweating"], "cf": 0.85,
     "text": "IF fever AND chills AND sweating THEN strongly suspect malaria "
             "(classic malaria paroxysm triad: cold stage, hot stage, sweating stage)"},
    {"id": "C2", "if": ["fever", "chills", "recent_travel"], "cf": 0.90,
     "text": "IF fever AND chills AND recent travel to an endemic area THEN very strongly "
             "suspect malaria"},
    {"id": "C3", "if": ["fever", "headache", "vomiting"], "cf": 0.60,
     "text": "IF fever AND headache AND vomiting THEN moderately suspect malaria "
             "(NOTE: overlaps with typhoid/viral illness - recommend differential testing)"},
    {"id": "C4", "if": ["fever", "vulnerable_group"], "cf": 0.55,
     "text": "IF fever AND patient is in a vulnerable group THEN escalate suspicion "
             "(children under 5, pregnant women, and immunocompromised patients "
             "progress to severe malaria faster)"},
]

ALL_RULES = BASE_RULES + COMPOUND_RULES

# -----------------------------------------------------------------------
# 4. THRESHOLDS for final classification
# -----------------------------------------------------------------------
THRESHOLDS = [
    (0.75, "High likelihood of malaria",
     "Symptom pattern strongly matches malaria. Recommend an urgent Rapid "
     "Diagnostic Test (RDT) or microscopy (blood smear) for confirmation, "
     "and clinical evaluation without delay."),
    (0.40, "Moderate likelihood of malaria",
     "Symptom pattern is consistent with possible malaria but is not "
     "conclusive. Recommend an RDT/microscopy test and monitor for "
     "worsening symptoms."),
    (0.0, "Low likelihood of malaria",
     "Symptom pattern does not strongly indicate malaria. Consider other "
     "differential diagnoses (e.g. typhoid, viral infection, flu). If "
     "symptoms persist or worsen, seek clinical evaluation and testing "
     "regardless, since malaria cannot be ruled out on symptoms alone."),
]


def classify(cf_value: float):
    """Return (label, advice, level) for a given combined certainty factor.
    level is a short css-friendly tag: 'high', 'moderate', or 'low'."""
    levels = ["high", "moderate", "low"]
    for (threshold, label, advice), level in zip(THRESHOLDS, levels):
        if cf_value >= threshold:
            return label, advice, level
    return THRESHOLDS[-1][1], THRESHOLDS[-1][2], "low"
