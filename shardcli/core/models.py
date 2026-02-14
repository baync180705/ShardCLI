from dataclasses import dataclass
from shardcli.engine import RiskReport

@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    return_code: int
    success: bool

@dataclass
class ShardResponse:
    """
    Final structured response returned by the orchestrator.
    """
    command: str | None
    explanation: str
    note: str | None
    risk_report: RiskReport | None
