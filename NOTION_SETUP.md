# Notion Setup

Use this file to mirror the MVP inside a real Notion workspace for your final hackathon demo.

## Database 1: Runbooks

Properties:

- `Name` — Title
- `Trigger Type` — Multi-select
- `System` — Select
- `Allowed Actions` — Multi-select
- `Requires Approval` — Checkbox
- `Risk Level` — Select
- `Status` — Select

Create a page called `Refund Resolution Operator` with this body:

```md
# Refund Resolution Operator

## Purpose
Safely process low-risk refunds using an approval-first workflow.

## Required inputs
- customer_id
- order_id
- reason

## Steps
1. Validate the requester identity and locate the order in the support admin portal.
2. Check the refund policy window, payment status, and prior refund history.
3. Summarize the intended action and request human approval before executing.
4. Issue the refund in the portal and capture evidence of the transaction.
5. Write the result, notes, and audit trail back to Notion.

## Do not do
- Never refund an order that already shows refunded.
- Never process a refund without approval.
- Never change unrelated account fields.

## Escalation rules
- Escalate if the order total is above $250.
- Escalate if fraud risk is flagged on the customer profile.
```

Create a second page called `VIP Escalation Operator` with the same property pattern and escalation-focused steps.

## Database 2: Jobs

Properties:

- `Title` — Title
- `Runbook` — Relation to Runbooks
- `Requester` — Email
- `Priority` — Select
- `Status` — Select
- `Approval Status` — Select
- `Risk Summary` — Text
- `Result Summary` — Text
- `Started At` — Date
- `Completed At` — Date

## Database 3: Approvals

Properties:

- `Job` — Relation to Jobs
- `Reviewer` — Person or text
- `Decision` — Select
- `Notes` — Text
- `Approved At` — Date

## Database 4: Audit Log

Properties:

- `Job` — Relation to Jobs
- `Step` — Title
- `Action` — Text
- `Outcome` — Select
- `Timestamp` — Date

## Live demo workflow in Notion

1. Put your runbook pages in `Runbooks`.
2. Let the app create `Jobs`.
3. Use `Approvals` to show the human checkpoint.
4. Use `Audit Log` to show the execution history.

This gives you a clean story: Notion stores policy, current work, approvals, and operating memory.
