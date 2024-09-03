import json
import os
import subprocess
import time


class Doctor:

    def check_java(self):
        command = "java -version"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_vscode(self):
        command = "code -v"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_git(self):
        command = "git --version"
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_cjx_path(self):
        with open(self.cjx_path, "r") as f:
            path = json.load(f)

        if path["cjxPath"] != "":
            return True
        else:
            return False

    def check_javafx(self):
        with open(self.cjx_path, "r") as f:
            path = json.load(f)

        utils_path_json = f"{path['cjxPath']}/src/config/vscode_config.json"

        try:
            with open(utils_path_json, "r") as f:
                utils_path = json.load(f)
            if os.path.exists(utils_path["javafxPath"]):
                return True
            else:
                return False
        except OSError as e:
            return False

    def handle_doctor_command(self):
        flags = [
            Doctor.check_java(self),
            Doctor.check_vscode(self),
            Doctor.check_git(self),
            Doctor.check_javafx(self),
        ]

        return flags

    def print_status(self):

        print("Checking your system ", end="")
        for _ in range(5):
            print(". ", end="", flush=True)
            time.sleep(0.2)
        print("\n")

        flags = Doctor.handle_doctor_command(self)

        installed = [
            "\033[1mJava is installed ✔️\033[0m",
            "\033[1mVisual Studio Code is installed ✔️\033[0m",
            "\033[1mGit is installed ✔️\033[0m",
            "\033[1mJavaFX is setup ✔️\033[0m",
        ]

        not_installed = [
            "\033[1mJava is not installed ❌ \033[0m",
            "\033[1mVisual Studio Code is not installed ❌ \033[0m",
            "\033[1mGit is not installed ❌ \033[0m",
            "\033[1mJavaFX is not setup ❌ \033[0m",
        ]

        for i in range(len(flags)):
            if flags[i] == True:
                print(installed[i])
            else:
                print(not_installed[i])
            time.sleep(0.2)
