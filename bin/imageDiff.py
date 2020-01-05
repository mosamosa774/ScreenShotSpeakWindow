import shutil
import subprocess

threshold = 1000


def isImageDifferent():
    res = False
    proc = subprocess.Popen(
        "wsl compare -metric RMSE screen.png prev_screen.png NULL", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_res = proc.communicate()
    try:
        if float(cmd_res[1].decode('utf-8').split(" ")[0]) >= threshold:
            res = True
    except:
        res = True
    return res


def copyCurrentImageAsPrevOne():
    shutil.copy("screen.png", "prev_screen.png")


if __name__ == "__main__":
    isImageDifferent()
