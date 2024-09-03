import argparse
from utils.file_download import FileDownloader
from utils.animator import Animator
import asyncio


class CJXUPDATE:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="CJX CLI - Update", prog="cjxupdate"
        )
        self.parser.add_argument(
            "-u", "--update", action="store_true", help="Update CJX CLI"
        )
        self.parser.add_argument(
            "-c", "--check", action="store_true", help="Check for updates"
        )
        self.args = None

    def run(self):
        try:
            self.parse_args()
            self.handle_command()
        except Exception as e:
            print(f"Error: {e}")

    def parse_args(self):
        self.args = self.parser.parse_args()

    def handle_command(self):
        if self.args.update:
            self.check_and_update("update")
        elif self.args.check:
            self.check_and_update("check")
        elif not self.args.update and not self.args.check:
            self.parser.print_help()

    def check_and_update(self, request):
        fd = FileDownloader()
        try:
            print_stat = f"{'Checking latest release':<25}"
            asyncio.run(Animator.animator(fd.check_version, print_stat, request, None))
        except KeyboardInterrupt:
            print(f"{'Cancelled by the user':<60}")


def main():
    cjxupdate = CJXUPDATE()
    cjxupdate.run()


if __name__ == "__main__":
    main()
