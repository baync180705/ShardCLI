import os
import shlex
from pathlib import Path
from typing import List

from shardcli.engine.policy.base import SecurityPolicy
from shardcli.engine.risk_types import RiskLevel, RiskReport

class RiskEngine:
    def __init__(self, policy: SecurityPolicy):
        self.policy = policy
        self.SHELL_OPERATORS = {'&&', '||', '|', ';', '>', '>>'}

    def analyze(self, command_str: str, cwd: str = os.getcwd()) -> RiskReport:
            # 1. Empty Check
            if not command_str or not command_str.strip():
                return RiskReport(RiskLevel.SAFE, "Empty command")

            # 2. Tokenization
            try:
                tokens = shlex.split(command_str)
            except ValueError:
                return RiskReport(RiskLevel.WARN, "Complex syntax (unbalanced quotes). Review carefully.")

            # 3. Run All Detectors
            reports = [
                self._check_sudo(tokens),
                self._check_shell_operation(tokens),
                self._check_verbs(tokens),
                self._check_paths(tokens, cwd)
            ]

            # 4. Consolidate Results
            return self._consolidate_reports(reports)

    def _check_sudo(self, tokens: List[str]) -> RiskReport:
        if tokens and tokens[0] == "sudo":
            if not self.policy.allow_sudo():
                return RiskReport(RiskLevel.BLOCK, "Sudo is disabled by policy.")
            return RiskReport(RiskLevel.WARN, "Privilege escalation (sudo) detected")
        
        return RiskReport(RiskLevel.SAFE, "No sudo detected")
    
    def _check_shell_operation(self, tokens: List[str]) -> RiskReport:
        for token in tokens:
            if token in self.SHELL_OPERATORS:
                if not self.policy.allow_shell_operators():
                    return RiskReport(RiskLevel.BLOCK, "Shell operators not allowed by policy.")
        
        return RiskReport(RiskLevel.SAFE, "Shell operators are safe.")


    def _check_verbs(self, tokens: List[str]) -> RiskReport:
        highest_risk = RiskLevel.SAFE
        reason = "Safe"

        for token in tokens:
            if token.startswith('-') or token.startswith('$') or token in self.SHELL_OPERATORS:
                continue
            
            if token in self.policy.get_banned_commands():
                return RiskReport(RiskLevel.BLOCK, f"Banned command detected: '{token}'")
            
            if token in self.policy.get_dangerous_commands():
                highest_risk = RiskLevel.WARN
                reason = f"Destructive command detected: '{token}'"

        return RiskReport(highest_risk, reason)

    def _check_paths(self, tokens: List[str], cwd: str) -> RiskReport:
        for token in tokens:
            if token.startswith('-') or token.startswith('$') or token in self.SHELL_OPERATORS:
                continue
            
            if len(token) < 2 and token != '/': 
                continue

            try:
                expanded = os.path.expandvars(os.path.expanduser(token))
                abs_path = Path(os.path.abspath(os.path.join(cwd, expanded)))
                
                for critical in self.policy.get_critical_paths():
                    if abs_path == critical or critical in abs_path.parents:
                        return RiskReport(
                            RiskLevel.BLOCK, 
                            f"Target '{token}' affects critical system path '{critical}'."
                        )
            except Exception:
                continue

        return RiskReport(RiskLevel.SAFE, "Paths appear safe")

    def _consolidate_reports(self, reports: List[RiskReport]) -> RiskReport:
        """
        Aggregates multiple reports into a single final verdict.
        Priority: BLOCK > WARN > SAFE
        """
        blocks = [r for r in reports if r.level == RiskLevel.BLOCK]
        warns = [r for r in reports if r.level == RiskLevel.WARN]

        # 1. Any BLOCK overrides everything else
        if blocks:
            combined_reason = " AND ".join(report.reason for report in blocks)
            return RiskReport(RiskLevel.BLOCK, combined_reason)

        # 2. If no blocks, combine all Warnings
        if warns:
            combined_reason = " AND ".join(r.reason for r in warns)
            return RiskReport(RiskLevel.WARN, combined_reason)

        # 3. Otherwise, Safe
        return RiskReport(RiskLevel.SAFE, "Command appears benign.")