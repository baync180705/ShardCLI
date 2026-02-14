from typing import Set
from pathlib import Path

from shardcli.engine.policy.base import SecurityPolicy

class StrictPolicy(SecurityPolicy):
    @property
    def name(self) -> str:
        return "STRICT (Read-Only / Safe Mode)"

    def get_banned_commands(self) -> Set[str]:
        return {
            # Filesystem Destructive
            'rm', 'mv', 'cp', 'dd', 'shred', 'mkfs', 'mke2fs', 'format',
            # System State
            'shutdown', 'reboot', 'halt', 'poweroff', 'init',
            # Permissions
            'chmod', 'chown', 'chgrp', 'usermod', 'useradd', 'userdel',
            # Network / Remote
            'ssh', 'scp', 'rsync', 'curl', 'wget', 'nc', 'netcat', 'nmap',
            # Shell / Scripting
            'sh', 'bash', 'zsh', 'python', 'perl', 'ruby', 'eval', 'exec'
        }

    def get_dangerous_commands(self) -> Set[str]:
        return {'touch', 'mkdir', 'nano', 'vim', 'vi'}

    def get_critical_paths(self) -> Set[Path]:
        return {
            Path('/etc'), Path('/usr'), Path('/var'), 
            Path('/bin'), Path('/sbin'), Path('/boot'), Path('/dev'), 
            Path('/sys'), Path('/proc'), Path('/opt'), Path('/root')
        }

    def allow_sudo(self) -> bool:
        return False

    def allow_shell_operators(self) -> bool:
        return False