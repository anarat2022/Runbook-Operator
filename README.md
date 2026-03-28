# Runbook Operator

Runbook Operator is a Notion MCP hackathon project that turns SOPs in Notion into safe, approval-driven action. A request comes in, the agent selects the right runbook, drafts an execution plan, pauses for human approval, executes the workflow, and writes the result back into the operating system of record.

The current default is a mock Notion gateway and a mock support admin portal so the workflow is demo-safe and works without credentials. The code also includes a clear integration boundary for swapping in real Notion MCP calls.

### What the demo does

1. Create a support job from the dashboard.
2. The app selects the matching runbook and generates a plan.
3. The job lands in the approval queue.
4. A reviewer approves the job.
5. The operator executes the workflow against the mock admin portal.
6. The result and audit trail appear on the dashboard.

### Quick start

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

### Then open:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)
- [http://127.0.0.1:8000/portal](http://127.0.0.1:8000/portal)

### Architecture

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



