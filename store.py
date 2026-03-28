from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


class DemoStore:
    """In-memory store for the hackathon demo."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.state = self._seed_state()

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

    def _seed_state(self) -> dict[str, Any]:
        refund_steps = [
            "Validate the requester identity and locate the order in the support admin portal.",
            "Check the refund policy window, payment status, and prior refund history.",
            "Summarize the intended action and request human approval before executing.",
            "Issue the refund in the portal and capture evidence of the transaction.",
            "Write the result, notes, and audit trail back to Notion.",
        ]
        escalation_steps = [
            "Locate the customer account and collect the relevant order history.",
            "Review the escalation policy and classify the issue severity.",
            "Prepare a clear escalation note for human approval.",
            "Escalate the case to Tier 2 and tag the owner.",
            "Sync the outcome and timeline back into Notion.",
        ]
        now = now_iso()
        runbooks = [
            {
                "id": "rbk_refund",
                "name": "Refund Resolution Operator",
                "trigger_types": ["refund", "billing", "support"],
                "system": "Support Admin Portal",
                "allowed_actions": ["lookup_order", "issue_refund", "add_internal_note"],
                "requires_approval": True,
                "risk_level": "Medium",
                "summary": "Handles low-risk refunds with explicit approval and a full audit trail.",
                "required_inputs": ["customer_id", "order_id", "reason"],
                "success_criteria": [
                    "Refund is issued exactly once.",
                    "Internal notes include the policy basis and approval details.",
                    "The job and audit timeline are synced back into Notion.",
                ],
                "steps": refund_steps,
                "do_not_do": [
                    "Never refund an order that already shows refunded.",
                    "Never process a refund without approval.",
                    "Never change unrelated account fields.",
                ],
                "escalation_rules": [
                    "Escalate if the order total is above $250.",
                    "Escalate if fraud risk is flagged on the customer profile.",
                ],
                "notion_status": "Ready",
                "updated_at": now,
            },
            {
                "id": "rbk_escalation",
                "name": "VIP Escalation Operator",
                "trigger_types": ["vip", "escalation", "angry_customer"],
                "system": "Support Admin Portal",
                "allowed_actions": ["lookup_order", "assign_owner", "tag_case", "add_internal_note"],
                "requires_approval": True,
                "risk_level": "High",
                "summary": "Routes high-sensitivity support issues to the correct escalation path.",
                "required_inputs": ["customer_id", "order_id", "reason"],
                "success_criteria": [
                    "Case is assigned to Tier 2.",
                    "Approval notes are preserved.",
                    "Customer context is captured in Notion.",
                ],
                "steps": escalation_steps,
                "do_not_do": [
                    "Do not issue refunds from the escalation runbook.",
                    "Do not close the case before assignment.",
                ],
                "escalation_rules": [
                    "Escalate immediately when sentiment is severe or press risk exists.",
                ],
                "notion_status": "Ready",
                "updated_at": now,
            },
        ]
        customers = [
            {
                "id": "cus_1001",
                "name": "Ava Johnson",
                "tier": "Pro",
                "email": "ava@example.com",
                "fraud_risk": False,
                "orders": [
                    {
                        "id": "ord_301",
                        "item": "Studio Subscription",
                        "total": 79,
                        "status": "Paid",
                        "refunded": False,
                        "case_status": "Open",
                        "internal_note": "",
                    }
                ],
            },
            {
                "id": "cus_1002",
                "name": "Liam Chen",
                "tier": "Enterprise",
                "email": "liam@example.com",
                "fraud_risk": False,
                "orders": [
                    {
                        "id": "ord_302",
                        "item": "Team Workspace",
                        "total": 349,
                        "status": "Paid",
                        "refunded": False,
                        "case_status": "Open",
                        "internal_note": "",
                    }
                ],
            },
            {
                "id": "cus_1003",
                "name": "Sofia Patel",
                "tier": "Starter",
                "email": "sofia@example.com",
                "fraud_risk": True,
                "orders": [
                    {
                        "id": "ord_303",
                        "item": "Starter Plan",
                        "total": 19,
                        "status": "Paid",
                        "refunded": False,
                        "case_status": "Open",
                        "internal_note": "",
                    }
                ],
            },
        ]
        jobs = [
            {
                "id": "job_seed_1",
                "title": "Refund request for Ava Johnson",
                "requester": "ops@demo.dev",
                "customer_id": "cus_1001",
                "order_id": "ord_301",
                "issue_type": "refund",
                "reason": "Duplicate charge complaint",
                "runbook_id": "rbk_refund",
                "runbook_name": "Refund Resolution Operator",
                "status": "Awaiting approval",
                "approval_status": "Pending",
                "risk_summary": "Eligible for automated handling with manual approval.",
                "execution_plan": [
                    "Locate Ava Johnson and verify order ord_301.",
                    "Check refund policy and prior refund history.",
                    "After approval, issue refund and add an internal note.",
                    "Update Notion with the result and supporting evidence.",
                ],
                "result_summary": "",
                "missing_inputs": [],
                "evidence": [],
                "created_at": now,
                "started_at": "",
                "completed_at": "",
                "notion_sync": "Drafted",
            }
        ]
        approvals = []
        audit_log = [
            {
                "id": "audit_seed_1",
                "job_id": "job_seed_1",
                "step": "Runbook selected",
                "action": "Mapped incoming refund request to Refund Resolution Operator.",
                "outcome": "Success",
                "timestamp": now,
                "source": "Mock Notion MCP",
            }
        ]
        return {
            "runbooks": runbooks,
            "customers": customers,
            "jobs": jobs,
            "approvals": approvals,
            "audit_log": audit_log,
        }

