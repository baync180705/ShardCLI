from enum import Enum
from dataclasses import dataclass

class RiskLevel(Enum):
    SAFE = "SAFE"
    WARN = "WARN"
    BLOCK = "BLOCK"

@dataclass
class RiskReport:
    level: RiskLevel
    reason: str