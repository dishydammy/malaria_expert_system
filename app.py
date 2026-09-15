from flask import Flask, render_template, request
from knowledge_base import SYMPTOMS
from inference_engine import infer

app = Flask(__name__)

# Group symptoms by their 'group' field, preserving definition order
def grouped_symptoms():
    groups = {}
    order = []
    for s in SYMPTOMS:
        if s["group"] not in groups:
            groups[s["group"]] = []
            order.append(s["group"])
        groups[s["group"]].append(s)
    return [(g, groups[g]) for g in order]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", groups=grouped_symptoms())


@app.route("/diagnose", methods=["POST"])
def diagnose():
    selected = set(request.form.getlist("symptoms"))
    result = infer(selected)

    # Build readable list of what the user selected, for the results page
    selected_labels = [s["label"] for s in SYMPTOMS if s["id"] in selected]

    return render_template(
        "result.html",
        result=result,
        selected_labels=selected_labels,
        selected_count=len(selected_labels),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
