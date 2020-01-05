from __future__ import print_function
import sys
from time import sleep

from desktopmagic.screengrab_win32 import (
    getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
    getRectAsImage, getDisplaysAsImages)

image_name = "screen.png"

# not used


def moveScreenShot():
    import shutil
    import os
    for file_name in os.listdir('C:/Users/oogar/OneDrive/画像/スクリーンショット'):
        if "png" in file_name:
            shutil.move("C:/Users/oogar/OneDrive/画像/スクリーンショット/" +
                        file_name, "screen.png")
            return True
    return False


def takeScreenShotByPrtSc():
    import pyautogui as agui
    agui.hotkey('win', 'PrtSc')
    Found = False
    while not Found:
        Found = moveScreenShot()
    print("get screenshot")


def takeCaptureByPySc(x1, y1, x2, y2):
    from pyscreenshot import grab
    print(x1, y1, x2, y2)
    screenshot = grab(bbox=[upper_left_x, upper_left_y,
                            bottom_right_x, bottom_right_y])
    screenshot.save(image_name)

# until here


def takeCapture(x1, y1, x2, y2):
    print(x1, y1, x2, y2)
    rect256 = getRectAsImage((x1, y1, x2, y2))
    rect256.save(image_name, format='png')


if __name__ == '__main__':
    upper_left_x = 0
    upper_left_y = 0
    bottom_right_x = 500
    bottom_right_y = 500
    args = sys.argv
    try:
        upper_left_x = int(args[1])
        upper_left_y = int(args[2])
        bottom_right_x = int(args[3])
        bottom_right_y = int(args[4])
    except:
        print("error")
        exit

    takeCapture(upper_left_x, upper_left_y, bottom_right_x, bottom_right_y)
