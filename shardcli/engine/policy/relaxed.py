from typing import Set
from pathlib import Path

from shardcli.engine.policy.base import SecurityPolicy

class RelaxedPolicy(SecurityPolicy):
    @property
    def name(self) -> str:
        return "RELAXED (Power User Mode)"

    def get_banned_commands(self) -> Set[str]:
        return {
             ':(){ :|:& };:', # Still block fork bombs
        }

    def get_dangerous_commands(self) -> Set[str]:
        return {
            'mkfs', 'dd', 'fdisk', 'rm' 
        }

    def get_critical_paths(self) -> Set[Path]:
        return {
            Path('/proc'),
            Path('/sys'),
            Path('/dev/mem'),
            Path('/dev/kmem')
        }

    def allow_sudo(self) -> bool:
        return True

    def allow_shell_operators(self) -> bool:
        return True