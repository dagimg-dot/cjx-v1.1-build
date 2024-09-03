import json
import subprocess


class Env:
    def setEnvVariable():
        cjx_path = ""

        with open("c:/.cjx/utils_cjx.json", "r") as f:
            data = json.load(f)

        cjx_path = data["cjxPath"]

        ps_script = f"""
            $envName = 'Path'
            $envValue = [System.Environment]::GetEnvironmentVariable($envName, 'User')
            $newPath = $envValue + "{cjx_path}"
            [System.Environment]::SetEnvironmentVariable($envName, $newPath, 'User')
            """

        try:
            subprocess.run(["powershell", "-Command", ps_script])
            print("\tCJX CLI path added to the environment variable successfully")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    Env.setEnvVariable()
