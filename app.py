from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from runbook_operator.orchestrator import RunbookOperator


app = Flask(__name__)
operator = RunbookOperator()


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/portal")
def portal() -> str:
    return render_template("portal.html")


@app.get("/api/state")
def get_state():
    return jsonify(operator.get_state())


@app.post("/api/jobs")
def create_job():
    payload = request.get_json(silent=True) or {}
    job = operator.create_job(payload)
    return jsonify(job), 201


@app.post("/api/jobs/<job_id>/approve")
def approve_job(job_id: str):
    payload = request.get_json(silent=True) or {}
    try:
        job = operator.approve_job(
            job_id=job_id,
            reviewer=payload.get("reviewer", "team lead"),
            decision=payload.get("decision", "approve"),
            notes=payload.get("notes", "Approved for execution."),
        )
        return jsonify(job)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/jobs/<job_id>/run")
def run_job(job_id: str):
    try:
        job = operator.execute_job(job_id)
        return jsonify(job)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/reset")
def reset():
    return jsonify(operator.reset())


if __name__ == "__main__":
    app.run(debug=False)
