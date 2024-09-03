import platform
from utils.os_handler import WindowsHandler
from utils.os_handler import LinuxHandler


def get_os_handler():
    system = platform.system()
    if system == "Windows":
        return WindowsHandler()
    elif system == "Linux":
        return LinuxHandler()
    else:
        raise NotImplementedError(f"OS {system} is not supported.")
