import subprocess
import sys

def main():
    rest = sys.argv[1:]  # capture any extra CLI args for `uv publish`
    subprocess.check_call(["uvx", "uvx-build"])
    subprocess.check_call(["uvx", "uvx-publish"] + rest)

if __name__ == "__main__":
    sys.exit(main())
