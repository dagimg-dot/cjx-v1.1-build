import os
import json
import subprocess
from tqdm import tqdm
import time


class JFXML:
    def create_jfxml(self):
        try:
            functions = [
                JFXML.create_gitignore,
                JFXML.create_readme,
                JFXML.vscode_folder,
                JFXML.create_launch_json,
                JFXML.create_settings_json,
                JFXML.create_bin_folder,
                JFXML.create_src_folder,
                JFXML.create_src_sub_folders,
                JFXML.create_java_package,
                JFXML.create_class,
                JFXML.create_resources_package,
                JFXML.create_main_fxml,
            ]

            success = True
            success &= JFXML.create_directory(self)

            if success:
                with tqdm(total=len(functions)) as pbar:
                    for func in functions:
                        success &= func(self)
                        pbar.update(1)
            else:
                return False

            return success
        except Exception as e:
            print(f"Error: {e}")
            return False

    def handle_jfxml(self):
        flag = JFXML.create_jfxml(self)
        if flag:
            print(
                f"\n\t\033[1mProject {self.project_name} created successfully 🎇\033[0m\n"
            )
        else:
            print(f"\t\033[1m ✖️  Error creating project {self.project_name} ✖️\033[0m\n")
            self.error_handling()

    def create_directory(self):
        try:
            time.sleep(0.2)
            new_folder = self.project_name
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)
                os.chdir(new_folder)
                command = "git init"
                try:
                    subprocess.check_output(
                        command, stderr=subprocess.STDOUT, shell=True
                    )
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
                    return False
                return True
            else:
                return False
        except OSError as e:
            print(f"Error creating directory: {e}")
            return False

    def create_gitignore(self):
        try:
            time.sleep(0.2)
            git_ignore = """            
# Ignore Visual Studio Code directory
.vscode/

# Ignore compiled binary files
bin/
        """

            with open(".gitignore", "w") as f:
                f.write(git_ignore)

            return True
        except OSError as e:
            print(f"Error creating .gitignore file: {e}")
            return False

    def create_readme(self):
        try:
            time.sleep(0.2)
            with open(f"{self.get_cjx_path()}/src/jfxml/README.md") as f:
                # print(os.getcwd())
                # with open('src/jfxml/README.md') as f:
                readme = f.read()

            readme = readme.replace(
                "project_name", f"Project Name: {self.project_name}"
            )

            with open("README.md", "w") as f:
                f.write(readme)
            return True
        except OSError as e:
            print(f"Error creating README.md file: {e}")
            return False

    def vscode_folder(self):
        try:
            time.sleep(0.2)
            os.mkdir(".vscode")
            return True
        except OSError as e:
            print(f"Error creating .vscode folder: {e}")
            return False

    def create_launch_json(self):
        try:
            time.sleep(0.2)
            with open(f"{self.get_cjx_path()}/src/jfxml/.vscode/launch.json", "r") as f:
                launch = json.load(f)

            with open(f"{self.get_cjx_path()}/utils/utils_path.json", "r") as f:
                constants = json.load(f)

            module_path = constants["javafxPath"] + "/lib"

            for config in launch["configurations"]:
                config["vmArgs"] = (
                    f'--module-path "{module_path}" --add-modules javafx.controls,javafx.fxml'
                )
                config["mainClass"] = f"com.{self.package_name}.App"

            with open(".vscode/launch.json", "w") as f:
                json.dump(launch, f, indent=4)

            return True

        except (OSError, json.JSONDecodeError) as e:
            print(f"Error creating launch.json file: {e}")
            return False

    def create_settings_json(self):
        try:
            time.sleep(0.2)
            with open(
                f"{self.get_cjx_path()}/src/jfxml/.vscode/settings.json", "r"
            ) as f:
                # with open('src/jfxml/.vscode/settings.json', 'r') as f:
                settings = json.load(f)

            # with open(f'{self.get_cjx_path()}/utils/utils_path.json', 'r') as f:
            with open(f"{self.get_cjx_path()}/utils/utils_path.json", "r") as f:
                constants = json.load(f)

            jar_path = constants["jarPath"]

            settings_filled = settings["java.project.referencedLibraries"] = []
            settings_filled.append("lib/**/*.jar")

            for jarfiles in constants["jarFiles"]:
                if not jarfiles.endswith(".jar"):
                    continue
                settings_filled.append(f"{jar_path}/{jarfiles}")

            with open(".vscode/settings.json", "w") as f:
                json.dump(settings, f, indent=4)

            return True

        except Exception as e:
            print(f"Error creating settings.json file: {e}")
            return False

    def create_bin_folder(self):
        try:
            time.sleep(0.2)
            os.mkdir("bin")
            return True
        except OSError as e:
            print(f"Error creating bin folder: {e}")
            return False

    def create_src_folder(self):
        try:
            time.sleep(0.2)
            os.mkdir("src")
            return True
        except OSError as e:
            print(f"Error creating src folder: {e}")
            return False

    def create_src_sub_folders(self):
        try:
            time.sleep(0.2)
            os.chdir("src")
            parent_dir = "main"
            os.mkdir(parent_dir)
            os.mkdir(f"{parent_dir}/java")
            os.mkdir(f"{parent_dir}/resources")
            return True
        except OSError as e:
            print(f"Error creating src folder: {e}")
            return False

    def create_java_package(self):
        try:
            time.sleep(0.2)
            os.chdir("main/java")
            os.mkdir("com")
            os.mkdir(f"com/{self.package_name}")
            return True
        except OSError as e:
            print(f"Error creating package in java folder: {e}")
            return False

    def create_resources_package(self):
        try:
            time.sleep(0.2)
            os.chdir("..")
            os.chdir("..")
            os.chdir("main/resources")
            os.mkdir("com")
            os.mkdir(f"com/{self.package_name}")
            return True
        except OSError as e:
            print(f"Error creating package resources folder: {e}")
            return False

    def create_class(self):
        try:
            time.sleep(0.2)
            with open(
                f"{self.get_cjx_path()}/src/jfxml/src/main/java/com/App.java.txt", "r"
            ) as f:
                app = f.read()

            app = app.replace("package_name", self.package_name)

            with open(f"com/{self.package_name}/App.java", "w") as f:
                f.write(app)

            with open(
                f"{self.get_cjx_path()}/src/jfxml/src/main/java/com/HelloWorldController.java.txt",
                "r",
            ) as f:
                controller = f.read()

            controller = controller.replace("package_name", self.package_name)

            with open(f"com/{self.package_name}/HelloWorldController.java", "w") as f:
                f.write(controller)

            return True
        except OSError as e:
            print(f"Error creating Class files: {e}")
            return False

    def create_main_fxml(self):
        try:
            with open(
                f"{self.get_cjx_path()}/src/jfxml/src/main/resources/com/HelloWorld.fxml.txt",
                "r",
            ) as f:
                fxml = f.read()

            fxml = fxml.replace("package_name", self.package_name)

            with open(f"com/{self.package_name}/HelloWorld.fxml", "w") as f:
                f.write(fxml)
            return True
        except OSError as e:
            print(f"Error creating FXML file: {e}")
            return False
