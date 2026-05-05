"""Architect agent that produces implementation plan."""
from typing import Dict, Any
from openai import OpenAI
from config import settings


class ArchitectAgent:
    """Creates architecture/implementation guidance for coding stage."""

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

    def design(self, query: str, workspace_path: str) -> Dict[str, Any]:
        """Build architecture plan for coding and testing stages."""
        system_prompt = """You are a software architect agent.
Create a concise implementation plan for a coding agent.
Focus on files to change, constraints, and test strategy."""
        user_prompt = (
            f"User request: {query}\n"
            f"Workspace path in shared volume: {workspace_path}\n\n"
            "Return a practical architecture plan."
        )
        completion = self.client.chat.completions.create(
            model=settings.default_llm_model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        response_text = completion.choices[0].message.content or ""
        return {
            "response": response_text,
            "workspace_path": workspace_path,
            "agent": "architect",
        }
