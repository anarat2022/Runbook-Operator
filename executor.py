from __future__ import annotations

from typing import Any

from runbook_operator.store import now_iso


class DemoExecutor:
    """Simulates the external admin portal actions for the MVP."""

    def execute(self, job: dict[str, Any], customers: list[dict[str, Any]]) -> tuple[str, list[str]]:
        customer = next((item for item in customers if item["id"] == job["customer_id"]), None)
        if not customer:
            return "Customer record was not found.", []

        order = next((item for item in customer["orders"] if item["id"] == job["order_id"]), None)
        if not order:
            return "Order record was not found.", []

        evidence = []
        if job["runbook_id"] == "rbk_refund":
            if order["refunded"]:
                return "Order was already refunded, so the workflow stopped safely.", evidence
            if order["total"] > 250 or customer["fraud_risk"]:
                return "Refund requires escalation due to policy rules.", evidence
            order["refunded"] = True
            order["case_status"] = "Resolved"
            order["internal_note"] = (
                f"Refund issued by Runbook Operator on {now_iso()} after human approval."
            )
            evidence = [
                f"Portal lookup completed for {customer['name']}.",
                f"Refund issued for {job['order_id']} totaling ${order['total']}.",
                "Internal note added to the account timeline.",
            ]
            return "Refund completed successfully and synced back into the job record.", evidence

        order["case_status"] = "Escalated to Tier 2"
        order["internal_note"] = (
            f"Case escalated by Runbook Operator on {now_iso()} after human approval."
        )
        evidence = [
            f"VIP case tagged for {customer['name']}.",
            f"Tier 2 escalation recorded for {job['order_id']}.",
            "Internal note added for the escalation owner.",
        ]
        return "Escalation completed and ownership was assigned.", evidence

