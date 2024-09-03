import json
import subprocess
import aiohttp
from tqdm import tqdm
import os
import requests
import shutil
import zipfile
from utils.animator import Animator


class FileDownloader:
    async def get_release(self):
        async with aiohttp.ClientSession() as session:
            url = (
                f"https://api.github.com/repos/dagimg-dot/cjx-cli-tool/releases/latest"
            )
            try:
                async with session.get(url) as response:
                    response_json = await response.json()
                    return response_json
            except aiohttp.ClientError as error:
                print(f"Error occurred while making request: {error}")
                return

    async def get_file_size(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_size = int(response.headers.get("Content-Length", 0))
                return file_size

    def get_currentversion(self):
        try:
            command = subprocess.run(["cjx", "--version"], stdout=subprocess.PIPE)
            current_version = command.stdout.decode("utf-8")
            current_version = "v" + current_version.split(" ")[1]
        except:
            print("CJX CLI not initialized yet")
            return

        return current_version

    async def check_version(self, request):
        response_j = await self.get_release()
        latest_version = response_j["tag_name"]
        current_version = self.get_currentversion()
        if float(latest_version.split("v")[1]) != float(current_version.split("v")[1]):
            print(f"A new version ({latest_version}) is available !")
            if request == "check":
                pass
            else:
                await self.zip_download(response_j, latest_version)
        else:
            print(f"You are using the latest version ({latest_version}).")

    async def zip_download(self, response_j, latest_version):
        init_path = "c:\.cjx"
        asset_url = response_j["assets"][0]["browser_download_url"]
        print_stat = f"{'Downloading the latest release ({}) : size => ':<30}".format(
            latest_version
        )
        try:
            total_size = await Animator.animator(
                self.get_file_size, print_stat, None, asset_url
            )
        except KeyboardInterrupt as e:
            print(f"{'Cancelled by the user':<60}")
            return
        block_size = 1024
        file_name = "cjx-{}.zip".format(latest_version)

        total_size_MB = round(total_size / (1000 * 1000), ndigits=3)
        print(f"{print_stat} {total_size_MB} MB")

        if not os.path.exists(init_path):
            print("CJX CLI not initialized yet")
            return

        os.chdir(init_path)
        if not os.path.exists("cache"):
            os.mkdir("cache")
            os.chdir(init_path + "\cache")
        else:
            os.chdir(init_path + "\cache")

        try:
            if os.path.exists(file_name):
                os.remove(file_name)

            response = requests.get(asset_url, stream=True)
            with open(file_name, "wb") as f:
                with tqdm(
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    miniters=1,
                    colour="green",
                ) as pbar:
                    for data in response.iter_content(block_size):
                        pbar.update(len(data))
                        f.write(data)

            print("\nDownload complete 💯")
            self.install_latest(init_path, file_name)

        except (requests.exceptions.RequestException, KeyboardInterrupt) as e:
            print("Error: ", e)

    def get_cjxpath(self, init_path):
        util = init_path + "\\utils_cjx.json"
        with open(util, "r") as f:
            data = json.load(f)

        cjx_path = data["cjxPath"]
        cjx_path = cjx_path[: cjx_path.rfind("/")]
        return cjx_path

    def install_latest(self, init_path, file_name):
        print("Installing the latest release...")
        cjx_path = self.get_cjxpath(init_path)
        os.chdir(cjx_path)
        if os.path.exists("cjx"):
            shutil.rmtree("cjx")
        else:
            pass
        os.chdir(init_path + "\cache")
        with zipfile.ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall(file_name.split(".zip")[0])
        os.chdir(file_name.split(".zip")[0])
        os.chdir(os.listdir()[0])
        shutil.move("cjx", cjx_path)
        print("Installation complete 💯")
        print("Restart the terminal to use the latest version")
        os.chdir(init_path + "\cache")
        shutil.rmtree(file_name.split(".zip")[0])
