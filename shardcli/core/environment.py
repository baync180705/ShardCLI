import os
import platform

try:
    import distro
except ImportError:
    distro = None


class Environment:
    def __init__(self):
        self.os = platform.system()
        self.distro = self._detect_distro()
        self.shell = self._detect_shell()
        self.shell_version = self._detect_shell_version()

    def _detect_distro(self):
        if self.os == "Linux" and distro:
            return distro.name(pretty=True)
        elif self.os == "Darwin":
            return "macOS"
        elif self.os == "Windows":
            return "Windows"
        return self.os

    def _detect_shell(self):
        if self.os == "Windows":
            return os.getenv("COMSPEC", "cmd")
        return os.getenv("SHELL", "unknown")

    def _detect_shell_version(self):
        if "bash" in str(self.shell):
            return os.getenv("BASH_VERSION")
        if "zsh" in str(self.shell):
            return os.getenv("ZSH_VERSION")
        return None
