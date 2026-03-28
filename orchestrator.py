from __future__ import annotations

from copy import deepcopy
from typing import Any
from uuid import uuid4

from runbook_operator.executor import DemoExecutor
from runbook_operator.notion_gateway import MockNotionGateway
from runbook_operator.store import DemoStore, now_iso


class RunbookOperator:
    def __init__(
        self,
        store: DemoStore | None = None,
        notion_gateway: MockNotionGateway | None = None,
        executor: DemoExecutor | None = None,
    ) -> None:
        self.store = store or DemoStore()
        self.notion_gateway = notion_gateway or MockNotionGateway()
        self.executor = executor or DemoExecutor()

    def get_state(self) -> dict[str, Any]:
        return self.store.snapshot()

    def reset(self) -> dict[str, Any]:
        self.store.reset()
        return self.get_state()

    def create_job(self, payload: dict[str, Any]) -> dict[str, Any]:
        issue_type = payload.get("issue_type", "refund").strip().lower()
        runbooks = self.notion_gateway.search_runbooks(self.store.state["runbooks"], issue_type)
        selected = deepcopy(runbooks[0])
        customer = self._find_customer(payload.get("customer_id", ""))
        title_name = customer["name"] if customer else payload.get("customer_id", "Unknown customer")
        job = {
            "id": f"job_{uuid4().hex[:8]}",
            "title": f"{issue_type.title()} request for {title_name}",
            "requester": payload.get("requester", "hackathon@demo.dev").strip() or "hackathon@demo.dev",
            "customer_id": payload.get("customer_id", "").strip(),
            "order_id": payload.get("order_id", "").strip(),
            "issue_type": issue_type,
            "reason": payload.get("reason", "").strip(),
            "runbook_id": selected["id"],
            "runbook_name": selected["name"],
            "status": "Awaiting approval",
            "approval_status": "Pending",
            "risk_summary": self._build_risk_summary(selected, customer),
            "execution_plan": self._build_execution_plan(selected, payload),
            "result_summary": "",
            "missing_inputs": self._missing_inputs(payload),
            "evidence": [],
            "created_at": now_iso(),
            "started_at": "",
            "completed_at": "",
            "notion_sync": "Pending",
        }
        self.store.state["jobs"].insert(0, job)
        self.notion_gateway.sync_job(job)
        self._append_audit(
            job["id"],
            "Job created",
            f"Created job using {selected['name']} for {payload.get('customer_id', 'unknown customer')}.",
            "Success",
        )
        return job

    def approve_job(self, job_id: str, reviewer: str, decision: str, notes: str) -> dict[str, Any]:
        job = self._find_job(job_id)
        approval = {
            "id": f"apr_{uuid4().hex[:8]}",
            "job_id": job_id,
            "reviewer": reviewer.strip() or "team lead",
            "decision": decision,
            "notes": notes.strip() or "Approved for execution.",
            "approved_at": now_iso(),
        }
        self.store.state["approvals"].insert(0, approval)
        self.notion_gateway.sync_approval(approval)
        job["approval_status"] = "Approved" if decision == "approve" else "Rejected"
        job["status"] = "Approved" if decision == "approve" else "Rejected"
        self.notion_gateway.sync_job(job)
        self._append_audit(
            job_id,
            "Human review",
            f"{approval['reviewer']} selected {approval['decision']}.",
            "Success",
        )
        return job

    def execute_job(self, job_id: str) -> dict[str, Any]:
        job = self._find_job(job_id)
        if job["approval_status"] != "Approved":
            raise ValueError("Job must be approved before execution.")

        job["status"] = "Running"
        job["started_at"] = now_iso()
        self.notion_gateway.sync_job(job)
        self._append_audit(job_id, "Execution started", "External workflow execution started.", "Success")

        result_summary, evidence = self.executor.execute(job, self.store.state["customers"])
        job["evidence"] = evidence
        job["result_summary"] = result_summary
        job["completed_at"] = now_iso()

        if "successfully" in result_summary.lower() or "completed" in result_summary.lower():
            job["status"] = "Completed"
            outcome = "Success"
        elif "stopped safely" in result_summary.lower():
            job["status"] = "Blocked"
            outcome = "Safe stop"
        else:
            job["status"] = "Needs escalation"
            outcome = "Escalated"

        self.notion_gateway.sync_job(job)
        for line in evidence or [result_summary]:
            self._append_audit(job_id, "Execution step", line, outcome)
        self._append_audit(job_id, "Execution finished", result_summary, outcome)
        return job

    def _build_execution_plan(self, runbook: dict[str, Any], payload: dict[str, Any]) -> list[str]:
        customer_id = payload.get("customer_id", "the customer")
        order_id = payload.get("order_id", "the order")
        steps = [
            f"Use Notion MCP to fetch the '{runbook['name']}' runbook.",
            f"Lookup customer {customer_id} and order {order_id} in the support admin portal.",
            "Evaluate policy constraints, prior actions, and safety rules.",
            "Pause for human approval before any irreversible action.",
        ]
        steps.extend(runbook["steps"][-2:])
        return steps

    def _build_risk_summary(self, runbook: dict[str, Any], customer: dict[str, Any] | None) -> str:
        risk = runbook["risk_level"]
        if not customer:
            return f"{risk} risk workflow. Customer context is still missing."
        if customer["fraud_risk"]:
            return f"{risk} risk workflow. Fraud flag detected, so escalation safeguards apply."
        return f"{risk} risk workflow. Eligible for approval-driven automation."

    def _missing_inputs(self, payload: dict[str, Any]) -> list[str]:
        missing = []
        for key in ("customer_id", "order_id", "reason"):
            if not payload.get(key):
                missing.append(key)
        return missing

    def _append_audit(self, job_id: str, step: str, action: str, outcome: str) -> None:
        entry = {
            "id": f"audit_{uuid4().hex[:8]}",
            "job_id": job_id,
            "step": step,
            "action": action,
            "outcome": outcome,
            "timestamp": now_iso(),
        }
        self.notion_gateway.sync_audit(entry)
        self.store.state["audit_log"].insert(0, entry)

    def _find_customer(self, customer_id: str) -> dict[str, Any] | None:
        return next(
            (item for item in self.store.state["customers"] if item["id"] == customer_id),
            None,
        )

    def _find_job(self, job_id: str) -> dict[str, Any]:
        job = next((item for item in self.store.state["jobs"] if item["id"] == job_id), None)
        if not job:
            raise ValueError(f"Unknown job '{job_id}'.")
        return job

