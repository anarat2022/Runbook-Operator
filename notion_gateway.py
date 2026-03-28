from __future__ import annotations

from typing import Any

from runbook_operator.store import now_iso


class MockNotionGateway:
    """A local stand-in for Notion MCP so the demo works instantly."""

    mode = "mock"

    def search_runbooks(self, runbooks: list[dict[str, Any]], issue_type: str) -> list[dict[str, Any]]:
        matches = [
            runbook
            for runbook in runbooks
            if issue_type.lower() in [value.lower() for value in runbook["trigger_types"]]
        ]
        return matches or runbooks

    def sync_job(self, job: dict[str, Any]) -> None:
        job["notion_sync"] = f"Synced at {now_iso()}"

    def sync_approval(self, approval: dict[str, Any]) -> None:
        approval["synced_via"] = "Mock Notion MCP"

    def sync_audit(self, entry: dict[str, Any]) -> None:
        entry["source"] = "Mock Notion MCP"


class LiveNotionGateway:
    """
    Integration contract for a real Notion MCP-backed implementation.

    The repo ships in mock mode so it is runnable without credentials, but this
    class makes the handoff to a live MCP client explicit in one place.
    """

    mode = "live"

    def __getattribute__(self, name: str) -> Any:  # pragma: no cover - intentional guardrail
        if name in {"mode", "__class__", "__doc__"}:
            return super().__getattribute__(name)
        raise NotImplementedError(
            "Live Notion MCP wiring is intentionally left as a narrow integration "
            "boundary. Replace LiveNotionGateway with your MCP client calls for "
            "search, fetch, page creation, and page updates."
        )

