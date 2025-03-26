"""
The Daytona SDK provides powerful process and code execution capabilities through
the `process` module in Sandboxes. This guide covers all available process operations
and best practices.

Example:
    Basic command execution:
    ```python
    sandbox = daytona.create()

    # Execute a shell command
    response = sandbox.process.exec("ls -la")
    print(response.result)

    # Run Python code
    response = sandbox.process.code_run("print('Hello, World!')")
    print(response.result)
    ```

    Using interactive sessions:
    ```python
    # Create a new session
    session_id = "my-session"
    sandbox.process.create_session(session_id)

    # Execute commands in the session
    req = SessionExecuteRequest(command="cd /workspace", var_async=False)
    sandbox.process.execute_session_command(session_id, req)

    req = SessionExecuteRequest(command="pwd", var_async=False)
    response = sandbox.process.execute_session_command(session_id, req)
    print(response.result)  # Should print "/workspace"

    # Clean up
    sandbox.process.delete_session(session_id)
    ```
"""

import json
from typing import List, Optional

from daytona_api_client import (
    Command,
    CreateSessionRequest,
    ExecuteRequest,
    Session,
    SessionExecuteRequest,
    SessionExecuteResponse,
    ToolboxApi,
)
from daytona_sdk._utils.errors import intercept_errors

from .charts import parse_chart
from .code_toolbox.sandbox_python_code_toolbox import SandboxPythonCodeToolbox
from .common.code_run_params import CodeRunParams
from .common.execute_response import ExecuteResponse, ExecutionArtifacts
from .protocols import SandboxInstance


class Process:
    """Handles process and code execution within a Sandbox.

    This class provides methods for executing shell commands and running code in
    the Sandbox environment.

    Attributes:
        code_toolbox (SandboxPythonCodeToolbox): Language-specific code execution toolbox.
        toolbox_api (ToolboxApi): API client for Sandbox operations.
        instance (SandboxInstance): The Sandbox instance this process belongs to.
    """

    def __init__(
        self,
        code_toolbox: SandboxPythonCodeToolbox,
        toolbox_api: ToolboxApi,
        instance: SandboxInstance,
    ):
        """Initialize a new Process instance.

        Args:
            code_toolbox (SandboxPythonCodeToolbox): Language-specific code execution toolbox.
            toolbox_api (ToolboxApi): API client for Sandbox operations.
            instance (SandboxInstance): The Sandbox instance this process belongs to.
        """
        self.code_toolbox = code_toolbox
        self.toolbox_api = toolbox_api
        self.instance = instance

    @staticmethod
    def _parse_output(lines: List[str]) -> Optional[ExecutionArtifacts]:
        """
        Parse the output of a command to extract ExecutionArtifacts.

        Args:
            lines: A list of lines of output from a command

        Returns:
            ExecutionArtifacts: The artifacts from the command execution
        """
        artifacts = ExecutionArtifacts("", [])
        for line in lines:
            if not line.startswith("dtn_artifact_k39fd2:"):
                artifacts.stdout += line
                artifacts.stdout += "\n"
            else:
                # Remove the prefix and parse JSON
                json_str = line.replace("dtn_artifact_k39fd2:", "", 1).strip()
                data = json.loads(json_str)
                data_type = data.pop("type")

                # Check if this is chart data
                if data_type == "chart":
                    chart_data = data.get("value", {})
                    artifacts.charts.append(parse_chart(**chart_data))

        return artifacts

    @intercept_errors(message_prefix="Failed to execute command: ")
    def exec(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> ExecuteResponse:
        """Execute a shell command in the Sandbox.

        Args:
            command (str): Shell command to execute.
            cwd (Optional[str]): Working directory for command execution. If not
                specified, uses the Sandbox root directory.
            timeout (Optional[int]): Maximum time in seconds to wait for the command
                to complete. 0 means wait indefinitely.

        Returns:
            ExecuteResponse: Command execution results containing:
                - exit_code: The command's exit status
                - result: Standard output from the command
                - charts: List of Chart objects if any charts were generated

        Example:
            ```python
            # Simple command
            response = sandbox.process.exec("echo 'Hello'")
            print(response.result)  # Prints: Hello

            # Command with working directory
            result = sandbox.process.exec("ls", cwd="/workspace/src")

            # Command with timeout
            result = sandbox.process.exec("sleep 10", timeout=5)
            ```
        """
        execute_request = ExecuteRequest(command=command, cwd=cwd, timeout=timeout)

        response = self.toolbox_api.execute_command(workspace_id=self.instance.id, execute_request=execute_request)

        # Post-process the output to extract ExecutionArtifacts
        artifacts = Process._parse_output(response.result.splitlines())

        # Create new response with processed output and charts
        # TODO: Remove model_construct once everything is migrated to pydantic # pylint: disable=fixme
        return ExecuteResponse.model_construct(
            exit_code=response.exit_code,
            result=artifacts.stdout,
            artifacts=artifacts,
            additional_properties=response.additional_properties,
        )

    def code_run(
        self, code: str, params: Optional[CodeRunParams] = None, timeout: Optional[int] = None
    ) -> ExecuteResponse:
        """Executes code in the Sandbox using the appropriate language runtime.

        Args:
            code (str): Code to execute.
            params (Optional[CodeRunParams]): Parameters for code execution.
            timeout (Optional[int]): Maximum time in seconds to wait for the code
                to complete. 0 means wait indefinitely.

        Returns:
            ExecuteResponse: Code execution result containing:
                - exit_code: The execution's exit status
                - result: Standard output from the code
                - charts: List of Chart objects if any charts were generated

        Example:
            ```python
            # Run Python code
            response = sandbox.process.code_run('''
                x = 10
                y = 20
                print(f"Sum: {x + y}")
            ''')
            print(response.result)  # Prints: Sum: 30
            ```
        """
        command = self.code_toolbox.get_run_command(code, params)
        return self.exec(command, timeout=timeout)

    @intercept_errors(message_prefix="Failed to create session: ")
    def create_session(self, session_id: str) -> None:
        """Create a new long-running background session in the Sandbox.

        Sessions are background processes that maintain state between commands, making them ideal for
        scenarios requiring multiple related commands or persistent environment setup. You can run
        long-running commands and monitor process status.

        Args:
            session_id (str): Unique identifier for the new session.

        Example:
            ```python
            # Create a new session
            session_id = "my-session"
            sandbox.process.create_session(session_id)
            session = sandbox.process.get_session(session_id)
            # Do work...
            sandbox.process.delete_session(session_id)
            ```
        """
        request = CreateSessionRequest(sessionId=session_id)
        self.toolbox_api.create_session(self.instance.id, create_session_request=request)

    @intercept_errors(message_prefix="Failed to get session: ")
    def get_session(self, session_id: str) -> Session:
        """Get a session in the Sandbox.

        Args:
            session_id (str): Unique identifier of the session to retrieve.

        Returns:
            Session: Session information including:
                - session_id: The session's unique identifier
                - commands: List of commands executed in the session

        Example:
            ```python
            session = sandbox.process.get_session("my-session")
            for cmd in session.commands:
                print(f"Command: {cmd.command}")
            ```
        """
        return self.toolbox_api.get_session(self.instance.id, session_id=session_id)

    @intercept_errors(message_prefix="Failed to get session command: ")
    def get_session_command(self, session_id: str, command_id: str) -> Command:
        """Get information about a specific command executed in a session.

        Args:
            session_id (str): Unique identifier of the session.
            command_id (str): Unique identifier of the command.

        Returns:
            Command: Command information including:
                - id: The command's unique identifier
                - command: The executed command string
                - exit_code: Command's exit status (if completed)

        Example:
            ```python
            cmd = sandbox.process.get_session_command("my-session", "cmd-123")
            if cmd.exit_code == 0:
                print(f"Command {cmd.command} completed successfully")
            ```
        """
        return self.toolbox_api.get_session_command(self.instance.id, session_id=session_id, command_id=command_id)

    @intercept_errors(message_prefix="Failed to execute session command: ")
    def execute_session_command(
        self,
        session_id: str,
        req: SessionExecuteRequest,
        timeout: Optional[int] = None,
    ) -> SessionExecuteResponse:
        """Executes a command in the session.

        Args:
            session_id (str): Unique identifier of the session to use.
            req (SessionExecuteRequest): Command execution request containing:
                - command: The command to execute
                - var_async: Whether to execute asynchronously

        Returns:
            SessionExecuteResponse: Command execution results containing:
                - cmd_id: Unique identifier for the executed command
                - output: Command output (if synchronous execution)
                - exit_code: Command exit status (if synchronous execution)

        Example:
            ```python
            # Execute commands in sequence, maintaining state
            session_id = "my-session"

            # Change directory
            req = SessionExecuteRequest(command="cd /workspace")
            sandbox.process.execute_session_command(session_id, req)

            # Create a file
            req = SessionExecuteRequest(command="echo 'Hello' > test.txt")
            sandbox.process.execute_session_command(session_id, req)

            # Read the file
            req = SessionExecuteRequest(command="cat test.txt")
            result = sandbox.process.execute_session_command(session_id, req)
            print(result.output)  # Prints: Hello
            ```
        """
        return self.toolbox_api.execute_session_command(
            self.instance.id,
            session_id=session_id,
            session_execute_request=req,
            _request_timeout=timeout or None,
        )

    @intercept_errors(message_prefix="Failed to get session command logs: ")
    def get_session_command_logs(self, session_id: str, command_id: str) -> str:
        """Get the logs for a command executed in a session.

        This method retrieves the complete output (stdout and stderr) from a
        command executed in a session. It's particularly useful for checking
        the output of asynchronous commands.

        Args:
            session_id (str): Unique identifier of the session.
            command_id (str): Unique identifier of the command.

        Returns:
            str: Complete command output including both stdout and stderr.

        Example:
            ```python
            # Execute a long-running command asynchronously
            req = SessionExecuteRequest(
                command="sleep 5; echo 'Done'",
                var_async=True
            )
            response = sandbox.process.execute_session_command("my-session", req)

            # Wait a bit, then get the logs
            import time
            time.sleep(6)
            logs = sandbox.process.get_session_command_logs(
                "my-session",
                response.command_id
            )
            print(logs)  # Prints: Done
            ```
        """
        return self.toolbox_api.get_session_command_logs(self.instance.id, session_id=session_id, command_id=command_id)

    @intercept_errors(message_prefix="Failed to list sessions: ")
    def list_sessions(self) -> List[Session]:
        """List all sessions in the Sandbox.

        Returns:
            List[Session]: List of all sessions in the Sandbox.

        Example:
            ```python
            sessions = sandbox.process.list_sessions()
            for session in sessions:
                print(f"Session {session.session_id}:")
                print(f"  Commands: {len(session.commands)}")
            ```
        """
        return self.toolbox_api.list_sessions(self.instance.id)

    @intercept_errors(message_prefix="Failed to delete session: ")
    def delete_session(self, session_id: str) -> None:
        """Delete an interactive session from the Sandbox.

        This method terminates and removes a session, cleaning up any resources
        associated with it.

        Args:
            session_id (str): Unique identifier of the session to delete.

        Example:
            ```python
            # Create and use a session
            sandbox.process.create_session("temp-session")
            # ... use the session ...

            # Clean up when done
            sandbox.process.delete_session("temp-session")
            ```
        """
        self.toolbox_api.delete_session(self.instance.id, session_id=session_id)
