# OLLAMA-LANGCHAING-AGENTE/core/agent_state.py
from typing import List, Tuple, TypedDict

class AgentState(TypedDict):
    """
    Represents the state of an agent in LangGraph.
    This can be extended by specific agents to include more fields.
    """
    messages: List[Tuple[str, str]]
    # Add other common state variables here as needed,
    # e.g., tool_outputs: List[str]
