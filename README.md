# Runbook Operator

Runbook Operator is a Notion MCP hackathon project that turns SOPs in Notion into safe, approval-driven action. A request comes in, the agent selects the right runbook, drafts an execution plan, pauses for human approval, executes the workflow, and writes the result back into the operating system of record.

This repo ships with a polished local MVP so you can demo the idea immediately. The current default is a mock Notion gateway and a mock support admin portal so the workflow is demo-safe and works without credentials. The code also includes a clear integration boundary for swapping in real Notion MCP calls.

## Why this is strong for the challenge

- It makes Notion the control plane instead of just a note store.
- It demonstrates MCP-style search, fetch, state updates, and human confirmation.
- It has visible technical depth: runbook selection, approvals, execution, and audit logging.
- It demos well because both the operator dashboard and the external system visibly change.

## What the demo does

1. Create a support job from the dashboard.
2. The app selects the matching runbook and generates a plan.
3. The job lands in the approval queue.
4. A reviewer approves the job.
5. The operator executes the workflow against the mock admin portal.
6. The result and audit trail appear on the dashboard.

## Quick start

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Then open:

- [http://127.0.0.1:5000](http://127.0.0.1:5000)
- [http://127.0.0.1:5000/portal](http://127.0.0.1:5000/portal)

## Architecture

### App surface

- `app.py`: Flask entrypoint and API routes.
- `templates/index.html`: main operator dashboard.
- `templates/portal.html`: mock external admin system.
- `static/app.js`: UI rendering and interactions.
- `static/styles.css`: demo styling.

### Core logic

- `runbook_operator/store.py`: seed data and in-memory demo state.
- `runbook_operator/orchestrator.py`: workflow orchestration.
- `runbook_operator/executor.py`: simulated execution engine.
- `runbook_operator/notion_gateway.py`: mock and live Notion integration boundary.

## Live Notion MCP handoff

The repo is intentionally wired so the live integration lives in one place: [`runbook_operator/notion_gateway.py`](/Users/anaratfatima/Documents/New%20project/runbook_operator/notion_gateway.py).

To turn this into a real Notion MCP submission:

1. Replace `MockNotionGateway` with a real client that:
   - searches for runbooks
   - fetches runbook pages
   - creates and updates job pages
   - writes approvals and audit comments
2. Use the official Notion MCP endpoint:
   - `https://mcp.notion.com/mcp`
3. Keep the approval gate in place. Notion’s current docs recommend human confirmation for safety-sensitive workflows.

## Suggested demo script

1. Open the operator dashboard and the admin portal side by side.
2. Explain that runbooks live in Notion and drive the plan.
3. Create a refund job for `cus_1001`.
4. Show the generated plan and approval queue.
5. Click `Approve & Execute`.
6. Show the portal updating to `Refunded: Yes` and `Case: Resolved`.
7. End on the audit timeline and explain that Notion becomes the operational memory.

## Submission framing

Use this one-liner:

> Runbook Operator turns Notion into an operational control plane: agents fetch SOPs from Notion, wait for human approval, execute real work, and sync the outcome back into the workspace.

Judging criteria mapping:

- Originality & Creativity: Notion becomes the live source of executable operations.
- Technical Complexity: approval workflow, orchestration, execution engine, and audit logging.
- Use of Underlying Technology: the workflow is designed around Notion MCP search/fetch/update patterns.

## Files for your submission

- [`README.md`](/Users/anaratfatima/Documents/New%20project/README.md): project overview and setup
- [`SUBMISSION.md`](/Users/anaratfatima/Documents/New%20project/SUBMISSION.md): ready-to-paste hackathon copy
- [`NOTION_SETUP.md`](/Users/anaratfatima/Documents/New%20project/NOTION_SETUP.md): exact Notion schema and content

