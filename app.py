from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from database import init_db, save_assessment, list_assessments, get_assessment, delete_assessment
from calculations import calculate_assessment, get_factors, insight_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-this-prototype-key-before-production"
init_db()

def parse_payload(form, scope="combined"):
    errors, entries = [], []
    entered_categories = []

    def optional_number(name, label):
        raw = form.get(name, "").strip()
        if raw == "":
            return 0.0
        try:
            value = float(raw)
            if value < 0: raise ValueError
            entered_categories.append(name)
            return value
        except ValueError:
            errors.append(f"{label} must be a non-negative number.")
            return 0
    electricity = optional_number("electricity_kwh", "Monthly electricity consumption") if scope in ("electricity", "combined") else 0.0
    waste = optional_number("waste_kg", "Household waste") if scope in ("waste", "combined") else 0.0

    if scope in ("transportation", "combined"):
        kinds, distances = form.getlist("transport_type[]"), form.getlist("distance_km[]")
        for index, (kind, distance) in enumerate(zip(kinds, distances), 1):
            if not kind and not distance.strip(): continue
            if kind not in get_factors()["transport"]:
                errors.append(f"Transportation entry {index} needs a valid type.")
                continue
            try:
                distance_value = float(distance)
                if distance_value < 0: raise ValueError
                entries.append({"transport_type": kind, "distance_km": distance_value})
                entered_categories.append("transportation")
            except ValueError:
                errors.append(f"Transportation distance {index} must be a non-negative number.")
    if not entered_categories and not errors:
        labels = {"electricity": "electricity", "transportation": "transportation", "waste": "household waste"}
        if scope in labels:
            errors.append(f"Enter a value for {labels[scope]} before calculating this category.")
        else:
            errors.append("Enter a value for electricity, transportation, or household waste to calculate a combined estimate.")
    return {"electricity_kwh": electricity, "waste_kg": waste, "entries": entries}, errors

@app.route("/")
def index(): return render_template("index.html")

@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        scope = request.form.get("calculation_scope", "combined")
        if scope not in {"electricity", "transportation", "waste", "combined"}:
            scope = "combined"
        payload, errors = parse_payload(request.form, scope)
        if errors:
            for error in errors: flash(error, "error")
            return render_template("calculate.html", factors=get_factors(), form=request.form), 400
        results = calculate_assessment(payload["electricity_kwh"], payload["entries"], payload["waste_kg"])
        assessment_id = save_assessment(payload, results)
        return redirect(url_for("assessment", assessment_id=assessment_id))
    return render_template("calculate.html", factors=get_factors(), form={})

@app.route("/assessment/<int:assessment_id>")
def assessment(assessment_id):
    data = get_assessment(assessment_id)
    if not data: abort(404)
    highest, suggestion = insight_for(data)
    return render_template("assessment.html", assessment=data, highest=highest, suggestion=suggestion)

@app.route("/dashboard")
def dashboard():
    assessments = list_assessments()
    summary = None
    if assessments:
        latest = assessments[0]
        values = {"Electricity": latest["electricity_emission"], "Transportation": latest["transport_emission"], "Waste": latest["waste_emission"]}
        summary = {"average": sum(item["total_emission"] for item in assessments) / len(assessments), "highest": max(values, key=values.get)}
    return render_template("dashboard.html", assessments=assessments, summary=summary)

@app.route("/history")
def history(): return render_template("history.html", assessments=list_assessments(request.args.get("sort", "date")))

@app.post("/assessment/<int:assessment_id>/delete")
def remove(assessment_id):
    flash("Assessment deleted." if delete_assessment(assessment_id) else "Assessment not found.", "success")
    return redirect(url_for("history"))

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/api/history")
def api_history(): return jsonify(list_assessments())

@app.route("/api/assessment/<int:assessment_id>")
def api_assessment(assessment_id):
    data = get_assessment(assessment_id)
    return jsonify(data) if data else (jsonify({"error": "Assessment not found"}), 404)

@app.errorhandler(404)
def not_found(error): return render_template("error.html", message="We couldn’t find that assessment or page."), 404

if __name__ == "__main__": app.run(debug=True)
