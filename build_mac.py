#!/usr/bin/env python3
import subprocess
import sys


def main() -> None:
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=StackedDataTable",
        "--windowed",
        "--onedir",
        "--add-data=src:src",
        "--hidden-import=webview",
        "--hidden-import=webview.platforms.cocoa",
        "--collect-all=webview",
        "--clean",
        "gui.py",
    ]
    subprocess.run(cmd, check=True)
    print("\n빌드 완료: dist/StackedDataTable.app")


if __name__ == "__main__":
    main()
