"""Coding agent that delegates implementation to OpenHands Python SDK."""
from typing import Dict, Any
from config import settings
from .openhands_sdk_runner import OpenHandsSDKRunner


class CodingAgent:
    """Calls OpenHands SDK to perform coding work in shared workspace."""

    def __init__(self):
        self.sdk_runner = OpenHandsSDKRunner()

    def _build_payload(self, query: str, architecture_output: Dict[str, Any], workspace_path: str) -> Dict[str, Any]:
        architecture_text = architecture_output.get("response", "")
        return {
            "task": query,
            "workspace_path": workspace_path,
            "context": {
                "architecture_plan": architecture_text,
            },
        }

    def execute(self, query: str, architecture_output: Dict[str, Any], workspace_path: str) -> Dict[str, Any]:
        """Send coding task to OpenHands SDK."""
        payload = self._build_payload(query, architecture_output, workspace_path)
        architecture_text = payload["context"]["architecture_plan"]
        prompt = (
            f"Implement the requested change in workspace {workspace_path}.\n\n"
            f"User task:\n{query}\n\n"
            f"Architecture plan:\n{architecture_text}\n\n"
            "Apply code changes directly in workspace and provide concise summary of changes."
        )
        run = self.sdk_runner.run(
            prompt=prompt,
            workspace_path=workspace_path,
            timeout_seconds=settings.openhands_timeout_seconds,
        )
        result = {
            "response": run["message"],
            "openhands_result": run["raw_result"],
            "workspace_path": workspace_path,
            "agent": "coding",
            "sdk_status": run["status"],
            "sdk_run_id": run["run_id"],
        }
        if not run["ok"]:
            result["error"] = run.get("error", "openhands_sdk_error")
        return result
