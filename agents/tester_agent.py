"""Tester agent for running checks in shared workspace."""
from typing import Dict, Any
from config import settings
from .openhands_sdk_runner import OpenHandsSDKRunner


class TesterAgent:
    """Runs test command in the shared workspace directory."""

    def __init__(self):
        self.sdk_runner = OpenHandsSDKRunner()

    def run_tests(self, query: str, coding_output: Dict[str, Any], workspace_path: str) -> Dict[str, Any]:
        """Execute configured test command via OpenHands SDK."""
        command = settings.tester_command
        coding_summary = coding_output.get("response", "")
        prompt = (
            f"Run tests in workspace {workspace_path}.\n\n"
            f"Command: {command}\n\n"
            f"Coding stage summary:\n{coding_summary}\n\n"
            "Execute the command, report pass/fail and include key stdout/stderr details."
        )
        run = self.sdk_runner.run(
            prompt=prompt,
            workspace_path=workspace_path,
            timeout_seconds=settings.tester_timeout_seconds,
        )
        passed = run["ok"] and run["status"] == "finished"
        result = {
            "response": run["message"] if passed else f"Tests failed.\n\n{run['message']}",
            "passed": passed,
            "return_code": 0 if passed else 1,
            "command": command,
            "workspace_path": workspace_path,
            "coding_context": coding_summary,
            "agent": "tester",
            "sdk_status": run["status"],
            "sdk_run_id": run["run_id"],
            "openhands_result": run["raw_result"],
        }
        if not run["ok"]:
            result["error"] = run.get("error", "openhands_sdk_error")
        return result
