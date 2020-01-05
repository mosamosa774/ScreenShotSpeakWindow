
import subprocess

not_remove_key = " not_remove"


def modifyCapture(option=""):
    subprocess.run("wsl ./tesseract.sh"+option, shell=True)


if __name__ == "__main__":
    modifyCapture(option=not_remove_key)
