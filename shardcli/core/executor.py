import subprocess
from shardcli.core.models import ExecutionResult

class CommandExecutor:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute(self, command: str) -> ExecutionResult:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            return ExecutionResult(
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                success=result.returncode == 0
            )

        except subprocess.TimeoutExpired as e:
            return ExecutionResult(
                stdout=e.stdout or "",
                stderr="Execution timed out.",
                return_code=-1,
                success=False
            )

        except Exception as e:
            return ExecutionResult(
                stdout="",
                stderr=str(e),
                return_code=-1,
                success=False
            )
