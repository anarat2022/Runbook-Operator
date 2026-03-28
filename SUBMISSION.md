# Submission Copy

## Project name

Runbook Operator

## Short description

Runbook Operator turns Notion into an operational control plane. Instead of asking an AI agent to guess what to do from a prompt, teams store their real SOPs in Notion. The agent retrieves the correct runbook, builds a structured execution plan, pauses for human approval, performs the task, and syncs the result and audit trail back into Notion.

## Problem

Operational work is scattered across docs, ticket queues, chat, and admin tools. Most AI assistants sit outside that workflow and act without grounded context. Teams need agents that can use the real source of truth, follow policy, and keep humans in control.

## Solution

We built a runbook-driven operator for support workflows. In this MVP, a support request comes in, the system identifies the correct Notion runbook, generates a plan, requests approval, executes the workflow against an admin portal, and records the outcome. Notion acts as the place where policy, state, and audit history live together.

## Why it is compelling

- It makes Notion executable, not passive.
- It keeps a human in the loop for safety.
- It creates a visible audit trail for every action.
- It is easy to adapt beyond support into recruiting, finance, sales ops, and engineering workflows.

## Tech stack

- Flask
- Vanilla JavaScript
- Structured orchestration layer in Python
- Mock support admin portal for demo execution
- Notion MCP integration boundary for live search/fetch/update wiring

## What we would wire next

- Live Notion MCP search and fetch for runbook selection
- Live Notion page creation and page updates for jobs and approvals
- Browser automation with Playwright for external systems
- Slack notifications for approval requests

## Demo flow

1. Create a new refund request.
2. The system selects the right runbook and drafts an execution plan.
3. A human reviewer approves the workflow.
4. The operator executes the action in the admin portal.
5. The result appears in the portal and the audit timeline updates.

## Judging criteria alignment

- Originality & Creativity: uses Notion as a real operational brain.
- Technical Complexity: combines runbook retrieval, orchestration, approval, execution, and audit logging.
- Use of Underlying Technology: explicitly designed around Notion MCP workflows and human-in-the-loop safety.

