"""Web interface for the CrediDSL validator and simulator."""

import csv
from io import StringIO
import os

from flask import Flask, Response, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from credidsl import (
    ACTIONS, DEFAULT_POLICY, DEMO_VARIANT, VARIABLES, DataError,
    MAX_POLICY_LENGTH, analyze, validate_application,
)
from simulation import CSV_SIZE, COLUMNS, read_cases, simulate, synthetic_cases, validation_study

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 256 * 1024
SAMPLE_VALUES = {"puntaje": "650", "ingreso_mensual": "2200", "ratio_deuda": "0.35"}


def render_page(*, status=200, **context):
    model = {
        "policy_a": DEFAULT_POLICY, "policy_b": DEMO_VARIANT, "values": SAMPLE_VALUES,
        "actions": ACTIONS, "variables": VARIABLES, "analysis": (), "mode": "",
        "simulation": None, "study": None, "error": None, "dataset": None,
        "policy_limit": MAX_POLICY_LENGTH,
    }
    model.update(context)
    return render_template("index.html", **model), status


@app.get("/")
def index():
    return render_page()


@app.post("/evaluate")
def evaluate_policy():
    mode = request.form.get("action", "case")
    policy_a = request.form.get("policy_a", request.form.get("rule", DEFAULT_POLICY))
    policy_b = request.form.get("policy_b", DEMO_VARIANT)
    values = {
        name: request.form.get(name, fallback)
        for name, fallback in SAMPLE_VALUES.items()
    }
    context = {"policy_a": policy_a, "policy_b": policy_b, "values": values, "mode": mode}
    if mode == "study":
        return render_page(**context, study=validation_study())
    if mode not in {"validate", "case", "batch", "compare"}:
        return render_page(**context, error="Selecciona una operación válida.", status=400)

    a = analyze(policy_a)
    b = analyze(policy_b) if mode == "compare" else None
    analysis = [("Política A", a)]
    if b is not None:
        analysis.append(("Política B", b))
    context["analysis"] = analysis

    if a.policy is None or (b is not None and b.policy is None):
        return render_page(**context, status=400)
    if mode == "validate":
        return render_page(**context)

    try:
        if mode == "case":
            cases = [("Caso manual", validate_application(values))]
            dataset = "Solicitud ficticia ingresada"
        else:
            uploaded = request.files.get("cases")
            if uploaded and uploaded.filename:
                cases = read_cases(uploaded.stream.read(CSV_SIZE + 1))
                dataset = "Solicitudes ficticias del CSV"
            else:
                cases = synthetic_cases()
                dataset = "Lote de 100 solicitudes ficticias"
    except DataError as error:
        return render_page(**context, error=str(error), status=400)

    result = simulate(a.policy, cases, b.policy if b is not None else None)
    return render_page(**context, simulation=result, dataset=dataset)


@app.errorhandler(RequestEntityTooLarge)
def too_large(error):
    return render_page(error="La solicitud es demasiado grande. El CSV admite hasta 128 KB.", status=413)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "CrediDSL", "mode": "academic-demo"}


@app.get("/api/demo")
def api_demo():
    a = analyze(DEFAULT_POLICY).policy
    b = analyze(DEMO_VARIANT).policy
    result = simulate(a, synthetic_cases(), b)
    return {
        "cases": result["cases"], "counts": result["counts_a"],
        "counts_b": result["counts_b"], "changed": result["changed"],
        "elapsed_ms": result["elapsed_ms"], "rule": DEFAULT_POLICY,
    }


@app.get("/api/validation-study")
def api_study():
    return validation_study()


@app.get("/demo.csv")
def demo_csv():
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=COLUMNS)
    writer.writeheader()
    for case_id, values in synthetic_cases():
        writer.writerow({"id": case_id, **values})
    return Response(
        output.getvalue(), content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="solicitudes-ficticias.csv"'},
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
