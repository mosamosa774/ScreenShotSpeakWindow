from PIL import Image, ImageDraw
import pystray

icon_exist = False


def resume(release_func):
    global icon_exist
    icon_exist = False
    release_func()
    icon.stop()


def generateTrayIcon(release_func):
    global icon, icon_exist
    icon_exist = True
    icon = pystray.Icon('Speak Screenshot')
    ico = Image.open("../src/icon.ico")
    icon.icon = ico
    icon.menu = pystray.Menu(pystray.MenuItem(
        'Resume',
        lambda: resume(release_func)))
    icon.run()


# if __name__ == "__main__":
#    generateTrayIcon()
