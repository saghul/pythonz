
class BuildingException(Exception):
    """General exception during building"""

class ShellCommandException(Exception):
    """General exception during shell command"""

class AlreadyInstalledException(Exception):
    """General exception during installing"""

class DownloadError(Exception):
    """Exception during download"""

