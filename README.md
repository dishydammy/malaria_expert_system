# Malaria Diagnosis Expert System - CSC 520 Group Project

A rule-based expert system that uses Certainty Factors (CFs) to provide
malaria diagnosis decision support. The application is built with Python
and Flask.

## Running the application

```
pip install -r requirements.txt
python3 app.py
```

After the application starts, open **http://localhost:5050** in a browser.

## Project structure

```
malaria_expert_system/
├── app.py                # Flask routes (UI layer)
├── knowledge_base.py      # Facts, rules, thresholds (the "expert knowledge")
├── inference_engine.py    # CF combination logic (the "reasoning")
├── templates/
│   ├── index.html          # Symptom input form
│   └── result.html         # Diagnosis + explanation output
└── static/
    └── style.css
```

This structure represents the four classic expert-system components:

| Component | File |
|---|---|
| Knowledge base | `knowledge_base.py` |
| Inference engine | `inference_engine.py` |
| User interface | `templates/`, `static/` |
| Explanation facility | `result.html` (lists every rule that fired and its CF) |

## Reasoning process

1. The user checks off symptoms/risk factors in the form.
2. `inference_engine.infer()` checks every rule in `knowledge_base.py`.
   A rule "fires" if all of its required conditions are in the user's
   selected set.
3. Each fired rule contributes a Certainty Factor. Multiple fired rules
   are combined using the standard formula for combining independent
   positive evidence:

   ```
   CF_combined = CF1 + CF2 * (1 - CF1)
   ```

  applied iteratively across all fired rules. This means each additional
  confirming symptom increases confidence, with diminishing returns as
  the CF approaches 1.0 (100%); it cannot mathematically exceed 1.0.
4. The final CF is mapped to one of three bands:
   - **≥ 75%** → High likelihood → urgent RDT/microscopy recommended
   - **40%–74%** → Moderate likelihood → testing recommended
   - **< 40%** → Low likelihood → consider other differentials
5. The result page lists every rule that fired, in descending order of
   contribution — this is the explanation facility.

## Knowledge base design

- **11 base rules**: one per individual symptom/risk factor (e.g. fever,
  chills, recent travel).
- **4 compound rules**: symptom combinations that are stronger clinical
  indicators than any single symptom alone (e.g. the classic fever +
  chills + sweating "paroxysm" pattern, or fever + chills + travel
  history).
- CF values were set based on general clinical literature on malaria
  symptom prevalence and specificity (fever and chills are weighted
  higher; headache and fatigue are weighted lower since they overlap
  heavily with other common illnesses).
- Compound rules intentionally note where a pattern overlaps with a
  differential diagnosis. For example, fever + headache + vomiting may also
  indicate typhoid. This overlap is an important limitation of the system.

## Testing and validation

The project includes `test_cases.py`, a validation script containing 11
hand-labeled cases. The script runs each case through the inference engine
and reports the resulting classification, expected classification, and
overall accuracy.

Run the validation script with:

```
python3 test_cases.py
```

## Limitations

This is an educational decision-support tool. It does **not** replace a
Rapid Diagnostic Test (RDT), microscopy, or clinical evaluation by a
qualified health worker. CF values are illustrative and not derived from
a clinically validated dataset.
