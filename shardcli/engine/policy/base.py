from abc import ABC, abstractmethod
from typing import Set
from pathlib import Path

class SecurityPolicy(ABC):
    """
    Abstract Base Class defining the contract for all security policies.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The display name of the policy (e.g., 'Strict Mode')."""
        pass

    @abstractmethod
    def get_banned_commands(self) -> Set[str]:
        """Returns a set of commands that are strictly forbidden."""
        pass

    @abstractmethod
    def get_dangerous_commands(self) -> Set[str]:
        """Returns commands that are allowed but require explicit confirmation."""
        pass

    @abstractmethod
    def get_critical_paths(self) -> Set[Path]:
        """Returns absolute paths that must NEVER be modified."""
        pass

    @abstractmethod
    def allow_sudo(self) -> bool:
        """Determines if privilege escalation is permitted."""
        pass

    @abstractmethod
    def allow_shell_operators(self) -> bool:
        """Determines if chaining (&&, ||, ;) or piping (|) is permitted."""
        pass