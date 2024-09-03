import argparse
import json
import os
from pathlib import Path
import re
from commands.simple import Simple
from commands.jfxml import JFXML
from commands.doctor import Doctor
from commands.clone import Clone
from helpers import os_identifier


class CJX:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="cjx", description="CJX CLI", usage="%(prog)s [command] [options]"
        )
        self.parser.add_argument(
            "--version", "-v", action="version", version="%(prog)s 3.3"
        )
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.doctor_parser = self.subparsers.add_parser(
            "doctor", help="checks if the necessary pre-requisites are installed"
        )
        self.clone_parser = self.subparsers.add_parser(
            "clone",
            help="clones a javafx github repo to your local machine and setting it up for you environment",
        )
        self.clone_parser.add_argument("url", help="url of the repo to be cloned")
        self.init_parser = self.subparsers.add_parser(
            "init", help="initializes the CJX CLI"
        )
        self.setup_parser = self.subparsers.add_parser(
            "setup", help="Setting up environment for JavaFX development"
        )
        self.setup_parser.add_argument("sdk_path", help="Path of the JavaFX SDK")
        self.create_parser = self.subparsers.add_parser(
            "create", help="Create a new JavaFX project"
        )
        self.create_subparsers = self.create_parser.add_subparsers(dest="project_type")
        self.simple_parser = self.create_subparsers.add_parser(
            "simple", help="Create a simple JavaFX project"
        )
        self.simple_parser.add_argument(
            "project_name", help="Name of the JavaFX project"
        )
        self.jfxml_parser = self.create_subparsers.add_parser(
            "jfxml", help="Create a JavaFX project with FXML"
        )
        self.jfxml_parser.add_argument(
            "project_name", help="Name of the JavaFX project"
        )
        self.os_handler = os_identifier.get_os_handler()
        self.args = None
        self.project_name = None
        self.cjx_path = None
        self.package_name = None
        self.repo_name = None

    def run(self):
        try:
            self.parse_args()
            self.handle_command()
        except Exception as e:
            print(f"Error: {e}")

    def parse_args(self):
        self.args = self.parser.parse_args()

    def init(self):
        # try:
        #     if not os.path.exists("c:/.cjx"):
        #         current_path = os.getcwd()
        #         os.chdir("c:/")
        #         os.mkdir(".cjx")
        #         os.chdir(".cjx")
        #         with open("utils_cjx.json", "w") as f:
        #             json.dump({}, f, indent=4)

        #         with open("utils_cjx.json", "r") as f:
        #             utils_cjx = json.load(f)

        #         utils_cjx["cjxPath"] = ""

        #         with open("utils_cjx.json", "w") as f:
        #             json.dump(utils_cjx, f, indent=4)
        #         print(self.cjx_logo("welcome"))
        #         print("\t\033[ J CJX CLI initialized successfully 🎉\033[0m")
        #         os.chdir(current_path)
        #         print("\t\033[ J Setting the path of CJX CLI . . .\033[0m")
        #         self.set_cjx_path()
        #         print("\tAdding CJX CLI path to the environment variable . . .")
        #         Env.setEnvVariable()
        #     else:
        #         print("Error: CJX CLI already initialized")
        # except Exception as e:
        #     print(f"Error: {e}")
        try:
            cjx_dir = self.os_handler.get_cjx_dir()
            if not os.path.exists(cjx_dir):
                current_path = os.getcwd()
                self.os_handler.create_cjx_dir()
                print(self.cjx_logo("welcome"))
                print("\t\033[ J CJX CLI initialized successfully 🎉\033[0m")
                os.chdir(current_path)
                print("\t\033[ J Setting the path of CJX CLI . . .\033[0m")
                # self.set_cjx_path()
            else:
                print("Error: CJX CLI already initialized")
        except Exception as e:
            print(f"Error: {e}")

    def cjx_logo(self, type="main"):
        main = r"""
         ___    _____  _    _     ___    _      _ 
        (  _ \ (___  )( )  ( )   (  _ \ ( )    (_)
        | ( (_)    | | \ \/ /    | ( (_)| |    | |
        | |  _  _  | |  )  (     | |  _ | |  _ | |
        | (_( )( )_| | / /\ \    | (_( )| |_( )| |
        (____/  \___/ ( )  (_)   (____/ ((___/ (_)
                      /(                (_)       
                     (__)                         
        """
        welcome = r"""
                        __                                     __          
        __  _  __ ____ |  |   ____   ____   _____   ____     _/  |_  ____  
        \ \/ \/ // __ \|  | _/ ___\ / __ \ /     \_/ __ \    \   __\/ __ \ 
        \     /\  ___/_  |__  \___(  \_\ )  | |  \  ___/_    |  | (  \_\ )
        \/\_/  \___  /____/\___  /\____/|__|_|  /\___  /    |__|  \____/ 
                    \/          \/             \/     \/                  
  
                                ┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃
                                ┃┃┃┃┃┃┃┏┓┃┃┃┃┃┃
                                ┏━━┓┃┃┃┗┛┃┃┃┓┏┓
                                ┃┏━┛┃┃┃┏┓┃┃┃╋╋┛
                                ┃┗━┓┃┃┃┃┃┃┃┃╋╋┓
                                ┗━━┛┃┃┃┃┃┃┃┃┛┗┛
                                ┃┃┃┃┃┃┃┛┃┃┃┃┃┃┃
                                ┃┃┃┃┃┃┃━┛┃┃┃┃┃┃
        """
        if type == "welcome":
            return welcome

        return main

    def handle_command(self):
        command = self.args.command
        if command == "init":
            self.init()
        elif command in ["create", "setup", "doctor", "clone"]:
            cjx_dir = self.os_handler.get_cjx_dir()
            if os.path.exists(cjx_dir):
                self.cjx_path = os.path.join(cjx_dir, "utils_cjx.json")
                if command == "create":
                    # if False in Doctor.handle_doctor_command(self):
                    #     print(
                    #         "Error: Please follow the instructions carefully, or run 'cjx doctor' to see what's wrong"
                    #     )
                    # else:
                    self.handle_create_command()
                elif command == "setup":
                    self.handle_setup_command()
                elif command == "doctor":
                    Doctor.print_status(self)
                elif command == "clone":
                    if False in Doctor.handle_doctor_command(self):
                        print(
                            "Error: Please follow the instructions carefully, or run 'cjx doctor' to see what's wrong"
                        )
                    else:
                        Clone.check_repo(self)
            else:
                print("Error: CJX CLI not initialized")
        elif command is None:
            print(self.cjx_logo())
            self.parser.print_help()
        else:
            print(f"Error: Invalid command: {command}")

    def handle_create_command(self):
        if self.args.project_type == "simple":
            self.project_name = self.args.project_name
            print(f"\n\tCreating simple JavaFX project {self.project_name}\n")
            Simple.handle_simple(self)
        elif self.args.project_type == "jfxml":
            self.project_name = self.args.project_name
            pak_name = input(
                f"Enter package name for project {self.project_name} (default: cjx): "
            )
            self.validity_checker(pak_name)
            print(
                f"\n\tCreating JavaFX project {self.project_name} with FXML support\n"
            )
            JFXML.handle_jfxml(self)
        else:
            print("Error: Invalid project type")

    def validity_checker(self, pak_name):
        java_keywords = [
            "abstract",
            "assert",
            "boolean",
            "break",
            "byte",
            "case",
            "catch",
            "char",
            "class",
            "const",
            "continue",
            "default",
            "do",
            "double",
            "else",
            "enum",
            "extends",
            "final",
            "finally",
            "float",
            "for",
            "if",
            "goto",
            "implements",
            "import",
            "instanceof",
            "int",
            "interface",
            "long",
            "native",
            "new",
            "package",
            "private",
            "protected",
            "public",
            "return",
            "short",
            "static",
            "strictfp",
            "super",
            "switch",
            "synchronized",
            "this",
            "throw",
            "throws",
            "transient",
            "try",
            "void",
            "volatile",
            "while",
        ]
        validinput = False
        while not validinput:
            if pak_name == "":
                self.package_name = "cjx"
                validinput = True
            else:
                try:
                    if (
                        not re.match(r"^[a-z]+(\.[a-z]+)*$", pak_name)
                        or pak_name[0].isdigit()
                        or pak_name[-1] == "."
                        or pak_name in java_keywords
                    ):
                        raise ValueError
                    else:
                        self.package_name = pak_name
                        validinput = True
                except ValueError:
                    print("Error: Invalid package name")
                    pak_name = input(
                        f"Enter package name for project {self.project_name} (default: cjx): "
                    )

    def handle_setup_command(self):
        if not os.path.exists(self.args.sdk_path):
            print("Error: JavaFX SDK not found")
        else:
            print("JavaFX SDK found")
            self.set_sdk_path(self.args.sdk_path)

    def set_sdk_path(self, sdk_path):
        try:
            with open(self.cjx_path, "r") as f:
                path = json.load(f)

            if path["cjxPath"] == "":
                print("Error: CJX CLI path not set")
            else:
                utils_path_json = f"{path['cjxPath']}/src/config/vscode_config.json"

                with open(utils_path_json, "r") as f:
                    utils_path = json.load(f)
                utils_path["javafxPath"] = sdk_path
                utils_path["jarPath"] = sdk_path + "/lib"
                with open(utils_path_json, "w") as f:
                    json.dump(utils_path, f, indent=4)

                print("JavaFX SDK path set successfully to", sdk_path)
        except:
            print("Error setting JavaFX SDK path")
            return

    def get_cjx_path(self):
        # with open(self.cjx_path, "r") as f:
            # path = json.load(f)
        # return path["cjxPath"]
        TEMPLATE_DIR = Path(__file__).parent.parent.parent
        return TEMPLATE_DIR

    def set_cjx_path(self):
        if self.os_handler.check_executable_path() or os.path.exists("cjx.py"):
            current_dir = os.getcwd()
            cjx_dir = self.os_handler.get_cjx_dir()
            try:
                with open(f"{cjx_dir}/utils_cjx.json", "r") as f:
                    path = json.load(f)

                current_dir = current_dir.replace("\\", "/")
                path["cjxPath"] = current_dir

                with open(f"{cjx_dir}/utils_cjx.json", "w") as f:
                    json.dump(path, f, indent=4)

                print("\tCJX CLI path set successfully to", current_dir)
            except:
                print(
                    "Error setting CJX path, check your current path. It has to be in the same directory as the dependencies folder."
                )
                return
        else:
            print(
                "Error: CJX executable not found, check your current path. It has to be in the same directory as the cjx executable."
            )
            return

    def error_handling(self):
        print("Possible reasons:")
        print("\t1. Project already exists")
        print("\t2. You don't have permission to create a project in this directory")
        print("\t3. You don't have git installed")


def main():
    cjx = CJX()
    cjx.run()


if __name__ == "__main__":
    main()
