# OLLAMA-LANGCHAING-AGENTE/tests/agents/git_specialist_test.py
import pytest
import os
import shutil
import asyncio
from unittest.mock import MagicMock, patch

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from agents.git_specialist.tools import git_specialist_tools, WORKSPACE_DIR, shell_tool, write_file_in_workspace, read_file_in_workspace
from agents.git_specialist.agent import git_specialist_graph
from core.persistence import get_checkpointer


# Setup and Teardown for tests
@pytest.fixture(scope="module", autouse=True)
def setup_test_environment():
    """Ensures a clean workspace for tests."""
    # Ensure WORKSPACE_DIR exists
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    
    # Yield control to tests
    yield
    
    # No extensive cleanup here for the workspace itself, individual tests clean their repos


@pytest.fixture
def test_repo_path():
    """Creates a temporary git repository for each test."""
    # Create a unique repo name to avoid conflicts during parallel testing
    repo_name = f"test_repo_{os.getpid()}_{asyncio.current_task().get_name() if asyncio.current_task() else 'sync'}"
    full_path = os.path.join(WORKSPACE_DIR, repo_name)
    
    # Initialize git repo
    os.makedirs(full_path, exist_ok=True)
    shell_tool.run(f"git init {full_path}")
    
    yield full_path
    
    # Clean up the repository after the test
    shutil.rmtree(full_path, ignore_errors=True)


# Test individual tools
def test_file_management_tools_exist():
    """Test that file management tools are correctly exposed."""
    assert write_file_in_workspace is not None
    assert read_file_in_workspace is not None

def test_git_tools_exist():
    """Test that git tools are correctly exposed."""
    assert len(git_specialist_tools) > 0
    tool_names = [tool.name for tool in git_specialist_tools]
    expected_git_tools = ["git_status", "git_add", "git_commit", "git_log"]
    for tool_name in expected_git_tools:
        assert tool_name in tool_names

@pytest.mark.asyncio
async def test_write_and_read_file(test_repo_path):
    """Test writing and reading a file using the workspace tools."""
    repo_basename = os.path.basename(test_repo_path)
    file_name = "test.txt"
    relative_file_path = os.path.join(repo_basename, file_name) # Path relative to WORKSPACE_DIR

    await asyncio.to_thread(
        write_file_in_workspace.invoke,
        file_path=relative_file_path,
        text="Hello from test!"
    )
    assert os.path.exists(os.path.join(test_repo_path, file_name))
    
    read_content = await asyncio.to_thread(
        read_file_in_workspace.invoke,
        file_path=relative_file_path
    )
    assert read_content == "Hello from test!"

@pytest.mark.asyncio
async def test_git_status_initial(test_repo_path):
    """Test initial git status."""
    repo_basename = os.path.basename(test_repo_path)
    git_status_tool = next(t for t in git_specialist_tools if t.name == "git_status")
    status_output = await asyncio.to_thread(
        git_status_tool.invoke,
        directory=repo_basename
    )
    assert "no commits yet" in status_output.lower()

@pytest.mark.asyncio
async def test_git_add_and_commit(test_repo_path):
    """Test git add and commit functionality."""
    repo_basename = os.path.basename(test_repo_path)
    file_name = "test_commit.txt"
    relative_file_path = os.path.join(repo_basename, file_name)
    
    await asyncio.to_thread(
        write_file_in_workspace.invoke,
        file_path=relative_file_path,
        text="Content for commit."
    )

    # Add file
    git_add_tool = next(t for t in git_specialist_tools if t.name == "git_add")
    add_output = await asyncio.to_thread(
        git_add_tool.invoke,
        file_pattern=file_name,
        directory=repo_basename
    )
    assert "the following paths are ignored" not in add_output.lower() # Check for no ignore errors

    # Commit file
    git_commit_tool = next(t for t in git_specialist_tools if t.name == "git_commit")
    commit_message = "feat: Add test_commit.txt"
    commit_output = await asyncio.to_thread(
        git_commit_tool.invoke,
        message=commit_message,
        directory=repo_basename
    )
    assert "1 file changed" in commit_output.lower()
    
    # Verify commit in log
    git_log_tool = next(t for t in git_specialist_tools if t.name == "git_log")
    log_output = await asyncio.to_thread(
        git_log_tool.invoke,
        directory=repo_basename,
        num_commits=1
    )
    assert commit_message in log_output

# Test agent invocation
@pytest.mark.asyncio
async def test_git_specialist_agent_invoke(test_repo_path):
    """Test the Git specialist agent's ability to process a request and use tools."""
    repo_basename = os.path.basename(test_repo_path)
    checkpointer = get_checkpointer("sqlite:///test_agent_memory.db")
    
    config = RunnableConfig(configurable={"thread_id": "agent-test-thread", "checkpoint": checkpointer})

    # The agent should respond by using git_status tool (or just outputting it directly)
    result = await git_specialist_graph.ainvoke(
        {"messages": [HumanMessage(content=f"What is the current status of the repository '{repo_basename}'?")]},
        config=config
    )
    
    # The response should contain tool_calls or directly the output of the status
    assert isinstance(result["messages"][-1], AIMessage)
    assert result["messages"][-1].tool_calls or "no commits yet" in result["messages"][-1].content.lower()


# To run tests: uv pip install pytest pytest-asyncio
# Then: uv pytest OLLAMA-LANGCHAING-AGENTE/tests/agents/git_specialist_test.py
