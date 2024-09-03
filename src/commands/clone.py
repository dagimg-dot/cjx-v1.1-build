import fnmatch
import json
import os
import subprocess
from commands.simple import Simple
from commands.jfxml import JFXML


class Clone:
    def file_search(self, file_extension, directory_path):
        isFound = False
        for root, dirnames, filenames in os.walk(directory_path):
            for _ in fnmatch.filter(filenames, file_extension):
                isFound = True
                break

        return isFound

    def check_repo(self):
        url = self.args.url
        self.repo_name = str(url.split("/")[-1].split(".")[0])
        Clone.clone_repo(self)

    def clone_repo(self):
        clone_command = f"git clone {self.args.url}"
        if os.path.exists(self.repo_name):
            print("Error: The repository you entered is already cloned")
            return
        try:
            subprocess.check_output(clone_command, shell=True)
            Clone.check_cloned_repo(self)
        except subprocess.CalledProcessError:
            print("Error: There is an error when cloning")

    def check_cloned_repo(self):
        os.chdir(self.repo_name)
        current_dir = os.getcwd()
        java_files_ext = "*.java"
        fxml_files_ext = "*.fxml"
        flag_x = Clone.file_search(self, fxml_files_ext, current_dir)
        flag_j = Clone.file_search(self, java_files_ext, current_dir)
        if flag_x == True and flag_j == True:
            Clone.add_config(self, "jfxml")
        elif flag_j:
            Clone.add_config(self, "simple")
        else:
            print("Error: The repository you cloned is not a javafx project !!")
            os.chdir("..")
            try:
                os.system(f"rmdir /s /q {self.repo_name}")
            except:
                os.system(f"Remove-Item {self.repo_name} -Recurse -Force")

    def add_config(self, project_type):
        if project_type == "simple":
            Simple.vscode_folder(self)
            Simple.create_launch_json(self)
            Simple.create_settings_json(self)

            Clone.config_packageName(self)

            print("\nJavaFX project cloned and configured successfully 🎇")
        elif project_type == "jfxml":
            JFXML.vscode_folder(self)
            JFXML.create_launch_json(self)
            JFXML.create_settings_json(self)

            Clone.config_packageName(self)

            print("\nJavaFX project cloned and configured successfully 🎇")

    def find_main_file(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf8") as f:
                        content = f.read()
                        if "public static void main(String" in content:
                            return file_path
        return None

    def config_packageName(self):
        main_file = Clone.find_main_file(os.getcwd())
        if main_file == None:
            print("Error: There is an error when configuring the project")
            return

        try:
            mainClass = main_file.split("src\\main\\java\\")[1].replace("\\", ".")[:-5]
        except:
            mainClass = main_file.split("src\\")[1].replace("\\", ".")[:-5]

        json_path = ".vscode/launch.json"

        try:
            with open(json_path, "r") as f:
                datas = json.load(f)

            for data in datas["configurations"]:
                data["mainClass"] = mainClass

            with open(json_path, "w") as f:
                json.dump(datas, f, indent=4)
        except:
            print("Error: There is an error when configuring the project")
