# OLLAMA-LANGCHAING-AGENTE/agents/git_specialist/tools.py
import os
from langchain.tools import tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import ShellTool
from typing import List

# Configure File Management Toolkit
# It's important to set a working_directory to confine file operations
# For now, we'll use a 'workspace' directory within our project.
# This ensures agents operate within a controlled sandbox.
# The `FileManagementToolkit` requires `tiktoken` to be installed.
# We already installed it as part of `langchain` dependencies.

# Ensure the workspace directory exists
WORKSPACE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

file_management_toolkit = FileManagementToolkit(
    root_dir=str(WORKSPACE_DIR),
    selected_tools=["read_file", "write_file", "list_directory", "file_delete"]
)
file_tools = file_management_toolkit.get_tools()

# Expose specific file tools as LangChain tools
# The toolkit returns tools as objects, let's make them callable for the agent directly
@tool
def read_file_in_workspace(file_path: str) -> str:
    """Read a file from the agent's workspace."""
    return file_tools[0].run(file_path) # Assuming read_file is the first tool

@tool
def write_file_in_workspace(file_path: str, text: str) -> str:
    """Write text to a file in the agent's workspace."""
    return file_tools[1].run({"file_path": file_path, "text": text}) # Assuming write_file is the second tool

@tool
def list_directory_in_workspace(path: str = ".") -> str:
    """List contents of a directory in the agent's workspace."""
    return file_tools[2].run(path) # Assuming list_directory is the third tool

@tool
def delete_file_in_workspace(file_path: str) -> str:
    """Delete a file in the agent's workspace."""
    return file_tools[3].run(file_path) # Assuming file_delete is the fourth tool


# Shell Tool for general commands, including Git.
# IMPORTANT: ShellTool allows arbitrary command execution. Use with extreme caution and sandboxing.
shell_tool = ShellTool()

# Define specific Git tools using shell_tool wrapper
@tool
def git_status(directory: str = ".") -> str:
    """
    Shows the working tree status.
    Args:
        directory (str): The directory (relative to workspace) to run git status in. Defaults to current directory of workspace.
    """
    # Using the shell_tool directly for simplicity, but in a real scenario,
    # it might be better to explicitly validate/sanitize `directory` input.
    full_path = os.path.join(WORKSPACE_DIR, directory)
    if not os.path.exists(full_path):
        return f"Error: Directory {directory} does not exist in workspace."
    return shell_tool.run(f"git -C {full_path} status")

@tool
def git_add(file_pattern: str, directory: str = ".") -> str:
    """
    Adds file contents to the index.
    Args:
        file_pattern (str): The file or pattern to add (e.g., "file.txt", "." for all changes).
        directory (str): The directory (relative to workspace) to run git add in. Defaults to current directory of workspace.
    """
    full_path = os.path.join(WORKSPACE_DIR, directory)
    if not os.path.exists(full_path):
        return f"Error: Directory {directory} does not exist in workspace."
    return shell_tool.run(f"git -C {full_path} add {file_pattern}")

@tool
def git_commit(message: str, directory: str = ".") -> str:
    """
    Records changes to the repository.
    Args:
        message (str): The commit message.
        directory (str): The directory (relative to workspace) to run git commit in. Defaults to current directory of workspace.
    """
    full_path = os.path.join(WORKSPACE_DIR, directory)
    if not os.path.exists(full_path):
        return f"Error: Directory {directory} does not exist in workspace."
    # Ensure message is properly quoted to handle spaces and special characters
    return shell_tool.run(f"git -C {full_path} commit -m '{message}'")

@tool
def git_push(remote: str = "origin", branch: str = "main", directory: str = ".") -> str:
    """
    Updates remote refs along with associated objects.
    Args:
        remote (str): The name of the remote to push to. Defaults to "origin".
        branch (str): The name of the branch to push. Defaults to "main".
        directory (str): The directory (relative to workspace) to run git push in. Defaults to current directory of workspace.
    """
    full_path = os.path.join(WORKSPACE_DIR, directory)
    if not os.path.exists(full_path):
        return f"Error: Directory {directory} does not exist in workspace."
    return shell_tool.run(f"git -C {full_path} push {remote} {branch}")

@tool
def git_pull(remote: str = "origin", branch: str = "main", directory: str = ".") -> str:
    """
    Fetches from and integrates with another repository or a local branch.
    Args:
        remote (str): The name of the remote to pull from. Defaults to "origin".
        branch (str): The name of the branch to pull. Defaults to "main".
        directory (str): The directory (relative to workspace) to run git pull in. Defaults to current directory of workspace.
    """
    full_path = os.path.join(WORKSPACE_DIR, directory)
    if not os.path.exists(full_path):
        return f"Error: Directory {directory} does not exist in workspace."
    return shell_tool.run(f"git -C {full_path} pull {remote} {branch}")

@tool
def git_log(num_commits: int = 5, directory: str = ".") -> str:
    """
    Shows commit logs.
    Args:
        num_commits (int): The number of commits to show. Defaults to 5.
        directory (str): The directory (relative to workspace) to run git log in. Defaults to current directory of workspace.
    """
    full_path = os.path.join(WORKSPACE_DIR, directory)
    if not os.path.exists(full_path):
        return f"Error: Directory {directory} does not exist in workspace."
    return shell_tool.run(f"git -C {full_path} log -n {num_commits} --oneline")

# Group all git-related tools
git_specialist_tools = [
    git_status,
    git_add,
    git_commit,
    git_push,
    git_pull,
    git_log,
    read_file_in_workspace,
    write_file_in_workspace,
    list_directory_in_workspace,
    delete_file_in_workspace,
]

if __name__ == "__main__":
    # Example usage (requires a git repo and Ollama to be running)
    print("--- Git Specialist Tools Test ---")

    # Create a dummy git repository for testing
    test_repo_name = "test_repo"
    test_repo_path = os.path.join(WORKSPACE_DIR, test_repo_name)
    
    # Clean up previous test repo if it exists
    if os.path.exists(test_repo_path):
        shell_tool.run(f"rm -rf {test_repo_path}")

    # Initialize git repo inside the workspace
    shell_tool.run(f"git init {test_repo_path}")
    print(f"Initialized git repo: {test_repo_path}")
    
    # Test writing a file using the workspace-confined tool
    write_file_in_workspace.invoke(file_path=os.path.join(test_repo_name, "README.md"), text="# Test Repo\nThis is a test repository for the Git Specialist Agent.")
    print(f"File created: {os.path.join(test_repo_path, 'README.md')}")

    # Test git status
    status_output = git_status.invoke(directory=test_repo_name)
    print(f"\nGit Status:\n{status_output}")

    # Test git add
    git_add.invoke({"file_pattern": "README.md", "directory": test_repo_name})
    status_output_after_add = git_status.invoke(directory=test_repo_name)
    print(f"\nGit Status after add:\n{status_output_after_add}")

    # Test git commit
    git_commit.invoke({"message": "Initial commit from agent", "directory": test_repo_name})
    status_output_after_commit = git_status.invoke(directory=test_repo_name)
    print(f"\nGit Status after commit:\n{status_output_after_commit}")

    # Test git log
    log_output = git_log.invoke(directory=test_repo_name)
    print(f"\nGit Log:\n{log_output}")

    # Test read file
    file_content = read_file_in_workspace.invoke(os.path.join(test_repo_name, "README.md"))
    print(f"\nREADME.md content:\n{file_content}")

    # Clean up test repo
    shell_tool.run(f"rm -rf {test_repo_path}")
    print(f"\nCleaned up test repo: {test_repo_path}")
