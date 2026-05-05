"""Router agent that determines which agent should handle the request."""
from typing import Dict, Any
from openai import OpenAI
from config import settings


class RouterAgent:
    """Routes requests to appropriate specialized agents."""
    
    def __init__(self):
        """Initialize router agent."""
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
    
    def route(self, query: str) -> Dict[str, Any]:
        """
        Determine which agent should handle the request.
        
        Args:
            query: User query
            
        Returns:
            Dict with 'agent' (agent name) and 'reasoning' (explanation)
        """
        system_prompt = """You are a routing agent for a fixed software-delivery pipeline.
The pipeline always starts with architect, then coding, then tester.
Return ONLY one word: architect."""

        completion = self.client.chat.completions.create(
            model=settings.default_llm_model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}"},
            ],
        )
        agent_name = (completion.choices[0].message.content or "").strip().lower()
        if agent_name != "architect":
            agent_name = "architect"
        
        return {
            "agent": agent_name,
            "reasoning": f"Routed to {agent_name} based on query analysis"
        }

