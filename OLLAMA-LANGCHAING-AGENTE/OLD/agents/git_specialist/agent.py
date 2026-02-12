# OLLAMA-LANGCHAING-AGENTE/agents/git_specialist/agent.py
import os
import sys

# Add the project root to sys.path to enable imports from 'core' and 'agents'
# Assuming the script is run from within the project structure
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import shutil
import asyncio
from typing import List, Tuple, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from core.factory import get_model
from core.persistence import get_checkpointer
from agents.git_specialist.tools import git_specialist_tools, WORKSPACE_DIR, shell_tool, write_file_in_workspace
from core.agent_state import AgentState as BaseAgentState # Using the base AgentState

# Extend the base AgentState for the Git Specialist if needed,
# though for now, the base AgentState is sufficient as it contains 'messages'.
class GitAgentState(BaseAgentState):
    """
    State for the Git Specialist Agent.
    """
    # Specific fields for Git operations could go here, e.g.,
    # current_repo_path: str = "."
    # last_git_output: str = ""
    pass

# Define the prompt for the Git Specialist Agent
git_specialist_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="""You are an expert Git and file system specialist. Your primary role is to assist in version control and file manipulation tasks within a designated workspace.
You have access to a suite of tools to perform Git commands (git_status, git_add, git_commit, git_push, git_pull, git_log) and basic file operations (read_file_in_workspace, write_file_in_workspace, list_directory_in_workspace, delete_file_in_workspace).
Always operate within the provided workspace context which is mounted at the root of your operations.
When asked to perform a Git operation, first analyze the current state using 'git_status' or 'list_directory_in_workspace' if necessary.
Be cautious with 'write_file_in_workspace' and 'delete_file_in_workspace'. Confirm the user's intent if the action seems destructive.
For commit messages, provide concise and descriptive text.
If a command fails, try to understand the error and suggest a corrective action or report the problem clearly.
You should respond directly with the output of the tools or a clear explanation of what you did or plan to do.
"""),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Initialize the model for the Git Specialist.
# Using a general model, could be refined to a more specific one if needed.
git_specialist_llm = get_model("default_ollama", "general")

# Bind tools to the LLM
git_specialist_llm_with_tools = git_specialist_llm.bind_tools(git_specialist_tools)

# Define the graph node for the Git Specialist Agent
def git_specialist_node(state: GitAgentState):
    """
    This node represents the core logic of the Git Specialist Agent.
    It takes the current state, processes the message, and uses tools if necessary.
    """
    # The LangChain agent handles the tool calling logic automatically.
    # The prompt and tools are bound to the LLM, and it decides what to do.
    response = git_specialist_llm_with_tools.invoke(git_specialist_prompt.format_messages(messages=state["messages"]))
    
    # Append the AI's response to the messages history
    return {"messages": state["messages"] + [response]}

# Build the LangGraph workflow for the Git Specialist
git_specialist_workflow = StateGraph(GitAgentState)

# Add the single node for the specialist
git_specialist_workflow.add_node("git_specialist", git_specialist_node)

# Define the entry and exit points
git_specialist_workflow.add_edge(START, "git_specialist")
git_specialist_workflow.add_edge("git_specialist", END) # Simple direct path for now

# Compile the graph
# The state_schema=GitAgentState is implicitly passed by StateGraph(GitAgentState)
git_specialist_graph = git_specialist_workflow.compile()

if __name__ == "__main__":
    # Example of how to run the Git Specialist Agent independently
    # Note: This will interact with the 'workspace' directory defined in tools.py
    
    # Create a checkpointer for the specialist agent
    checkpointer = get_checkpointer("sqlite:///git_specialist_memory.db")

    async def run_git_specialist_test():
        print("--- Running Git Specialist Agent Test ---")
        
        # Ensure a test repository exists in the workspace
        test_repo_name = "agent_test_repo"
        test_repo_full_path = os.path.join(WORKSPACE_DIR, test_repo_name)
        
        # Clean up previous test repo if it exists
        if os.path.exists(test_repo_full_path):
            shutil.rmtree(test_repo_full_path)
            print(f"Cleaned up existing test repo: {test_repo_full_path}")

        # Initialize git repo inside the workspace
        os.makedirs(test_repo_full_path) # Create the directory first
        shell_tool.run(f"git init {test_repo_full_path}")
        print(f"Initialized git repo: {test_repo_full_path}")

        config = RunnableConfig(configurable={"thread_id": "git-test-thread", "checkpoint": checkpointer})

        # Initial interaction: check status
        result = await git_specialist_graph.ainvoke(
            {"messages": [HumanMessage(content=f"What is the status of the repository in '{test_repo_name}'?")]},
            config=config
        )
        print("\n--- Git Specialist Response (Status) ---")
        print(result["messages"][-1].content)

        # Add a file
        await asyncio.to_thread(
            write_file_in_workspace.invoke,
            {"file_path": os.path.join(test_repo_name, "test_file.txt"), "text": "Hello Git!"}
        )
        
        result = await git_specialist_graph.ainvoke(
            {"messages": [HumanMessage(content=f"Add test_file.txt to the index in '{test_repo_name}'.")]},
            config=config
        )
        print("\n--- Git Specialist Response (Add) ---")
        print(result["messages"][-1].content)

        # Commit the file
        result = await git_specialist_graph.ainvoke(
            {"messages": [HumanMessage(content=f"Commit changes with message 'Add test_file' in '{test_repo_name}'.")]},
            config=config
        )
        print("\n--- Git Specialist Response (Commit) ---")
        print(result["messages"][-1].content)
        
        # Clean up
        shutil.rmtree(test_repo_full_path)
        print(f"\nCleaned up test repo: {test_repo_full_path}")

    # To run this example, ensure you have an event loop running.
    # For simple testing in a script, you can use:
    asyncio.run(run_git_specialist_test())
    print("\nTo test independently, uncomment `asyncio.run(run_git_specialist_test())` and ensure your environment is set up.")
