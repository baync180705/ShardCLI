from typing import Set
from pathlib import Path

from shardcli.engine.policy.base import SecurityPolicy

class DefaultPolicy(SecurityPolicy):
    @property
    def name(self) -> str:
        return "DEFAULT (Developer Safe Mode)"

    def get_banned_commands(self) -> Set[str]:
        return {
            'mkfs', 'mke2fs', 'fdisk', 'parted',  # Disk formatting
            'dd',  # Raw device writing
            'shutdown', 'reboot', 'init', # System power
            ':(){ :|:& };:', # Fork bombs
            'rm -rf /', # Specific signatures (handled by engine logic usually, but good to list verbs)
        }

    def get_dangerous_commands(self) -> Set[str]:
        return {
            'rm', 'mv', 'chmod', 'chown', 'systemctl', 'service', 
            'kill', 'pkill', 'killall', 'rsync', 'scp', 'ssh'
        }

    def get_critical_paths(self) -> Set[Path]:
        return {
            Path('/etc'), 
            Path('/usr'), 
            Path('/var/lib'), # Protect DBs but maybe allow /var/log
            Path('/boot'), 
            Path('/bin'), 
            Path('/sbin'),
            Path('/dev'),
            Path('/sys'),
            Path('/proc')
        }

    def allow_sudo(self) -> bool:
        return False

    def allow_shell_operators(self) -> bool:
        return True