"""LangGraph orchestrator for multi-agent system."""
from typing import TypedDict, Annotated, Any
import operator
from langgraph.graph import StateGraph, END
from agents import (
    RouterAgent,
    ArchitectAgent,
    CodingAgent,
    TesterAgent,
    CriticAgent
)
from config import settings


class AgentState(TypedDict):
    """State shared across all agents."""
    query: str
    routed_agent: str
    agent_response: dict
    all_responses: Annotated[list, operator.add]
    final_response: str
    verified: bool
    critic_verification: dict
    iteration: int
    workspace_path: str
    architecture_output: dict
    coding_output: dict
    testing_output: dict
    pipeline_trace: Annotated[list, operator.add]


class LangGraphOrchestrator:
    """Main orchestrator using LangGraph."""
    
    def __init__(self):
        """Initialize orchestrator with all agents."""
        self.router = RouterAgent()
        self.architect_agent = ArchitectAgent()
        self.coding_agent = CodingAgent()
        self.tester_agent = TesterAgent()
        self.critic = CriticAgent()
        
        # Build graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", self._router_node)
        workflow.add_node("architect", self._architect_node)
        workflow.add_node("coding", self._coding_node)
        workflow.add_node("tester", self._tester_node)
        workflow.add_node("critic", self._critic_node)
        workflow.add_node("aggregate", self._aggregate_node)
        
        # Set entry point
        workflow.set_entry_point("router")
        
        workflow.add_edge("router", "architect")
        workflow.add_edge("architect", "coding")
        workflow.add_edge("coding", "tester")
        workflow.add_edge("tester", "critic")
        
        # Critic goes to aggregate
        workflow.add_edge("critic", "aggregate")
        
        # Aggregate is the end
        workflow.add_edge("aggregate", END)
        
        return workflow
    
    def _router_node(self, state: AgentState) -> AgentState:
        """Router node - currently always starts pipeline with architect."""
        routing = self.router.route(
            state["query"]
        )
        return {
            "routed_agent": routing["agent"],
            "pipeline_trace": [{"stage": "router", "decision": routing}],
        }
    
    def _architect_node(self, state: AgentState) -> AgentState:
        """Architect agent node."""
        response = self.architect_agent.design(
            query=state["query"],
            workspace_path=state.get("workspace_path", settings.workspace_path),
        )
        return {
            "architecture_output": response,
            "agent_response": response,
            "all_responses": [response],
            "pipeline_trace": [
                {
                    "stage": "architect",
                    "result": response.get("response", ""),
                    "sdk_status": response.get("sdk_status", "n/a"),
                    "sdk_run_id": response.get("sdk_run_id"),
                }
            ],
        }
    
    def _coding_node(self, state: AgentState) -> AgentState:
        """Coding agent node (OpenHands integration)."""
        architecture = state.get("architecture_output", {})
        response = self.coding_agent.execute(
            query=state["query"],
            architecture_output=architecture,
            workspace_path=state.get("workspace_path", settings.workspace_path),
        )
        return {
            "coding_output": response,
            "agent_response": response,
            "all_responses": [response],
            "pipeline_trace": [
                {
                    "stage": "coding",
                    "result": response.get("response", ""),
                    "sdk_status": response.get("sdk_status", "unknown"),
                    "sdk_run_id": response.get("sdk_run_id"),
                }
            ],
        }

    def _tester_node(self, state: AgentState) -> AgentState:
        """Tester agent node."""
        coding_output = state.get("coding_output", {})
        response = self.tester_agent.run_tests(
            query=state["query"],
            coding_output=coding_output,
            workspace_path=state.get("workspace_path", settings.workspace_path),
        )
        return {
            "testing_output": response,
            "agent_response": response,
            "all_responses": [response],
            "pipeline_trace": [
                {
                    "stage": "tester",
                    "result": response.get("response", ""),
                    "sdk_status": response.get("sdk_status", "unknown"),
                    "sdk_run_id": response.get("sdk_run_id"),
                }
            ],
        }
    
    def _critic_node(self, state: AgentState) -> AgentState:
        """Critic/verifier node."""
        agent_response = state.get("agent_response", {})
        verification = self.critic.verify(
            state["query"],
            agent_response.get("response", ""),
            agent_response.get("agent", "unknown"),
            agent_response
        )
        return {
            "verified": verification["verified"],
            "critic_verification": verification,
            "agent_response": {**agent_response, "verification": verification}
        }
    
    def _aggregate_node(self, state: AgentState) -> AgentState:
        """Response aggregation node."""
        all_responses = state.get("all_responses", [])
        if not all_responses:
            all_responses = [state.get("agent_response", {})]
        
        aggregated = self.critic.aggregate_responses(all_responses, state["query"])
        verification = state.get("critic_verification", {})
        if verification and "verification" not in aggregated:
            aggregated = {**aggregated, "verification": verification}
        return {
            "final_response": aggregated.get("response", ""),
            "agent_response": aggregated
        }
    
    def invoke(self, query: str, workspace_path: str | None = None) -> dict[str, Any]:
        """
        Process a request through the orchestrator.
        
        Args:
            query: User query
            
        Returns:
            Final response dict
        """
        initial_state = {
            "query": query,
            "routed_agent": "",
            "agent_response": {},
            "all_responses": [],
            "final_response": "",
            "verified": False,
            "critic_verification": {},
            "iteration": 0,
            "workspace_path": workspace_path or settings.workspace_path,
            "architecture_output": {},
            "coding_output": {},
            "testing_output": {},
            "pipeline_trace": [],
        }
        
        result = self.app.invoke(initial_state)
        return result

