from abc import ABC, abstractmethod
import json
import os


class OSHandler(ABC):
    @abstractmethod
    def get_home_dir(self):
        pass

    @abstractmethod
    def get_cjx_dir(self):
        pass

    @abstractmethod
    def create_cjx_dir(self):
        pass

    @abstractmethod
    def set_env_variable(self):
        pass

    @abstractmethod
    def check_executable_path(self):
        pass


class WindowsHandler(OSHandler):
    home_dir = "c:/"

    def get_home_dir(self):
        return self.home_dir

    def get_cjx_dir(self):
        return f"{self.home_dir}/.cjx"

    def create_cjx_dir(self):
        os.chdir(self.get_home_dir())
        os.mkdir(".cjx")
        # Create a configuration file in the cjx directory
        with open(os.path.join(self.get_cjx_dir(), "utils_cjx.json"), "w") as f:
            json.dump({"cjxPath": ""}, f, indent=4)

    def check_executable_path(self):
        if os.path.exists("cjx.exe"):
            return True
        return False

    def set_env_variable(self):
        print("Setting environment variable in Windows")


class LinuxHandler(OSHandler):
    home_dir = os.environ.get("HOME")

    def get_home_dir(self):
        return self.home_dir

    def get_cjx_dir(self):
        return f"{self.home_dir}/.cjx"

    def create_cjx_dir(self):
        os.chdir(self.get_home_dir())
        os.mkdir(".cjx", mode=0o755, dir_fd=None)
        # Create a configuration file in the cjx directory
        with open(os.path.join(self.get_cjx_dir(), "utils_cjx.json"), "w") as f:
            json.dump({"cjxPath": ""}, f, indent=4)

    def check_executable_path(self):
        if os.path.exists("cjx"):
            return True
        return False

    def set_env_variable(self):
        print("Setting environment variable in Linux")
