from PIL import Image, ImageDraw
import pystray

icon_exist = False

def resume():
    global icon_exist
    icon_exist = False
    icon.stop()


def generateTrayIcon():
    global icon, icon_exist
    icon_exist = True
    icon = pystray.Icon('Speak Screenshot')
    ico = Image.open("../src/icon.ico")
    icon.icon = ico
    icon.menu = pystray.Menu(pystray.MenuItem(
        'Resume',
        resume))
    icon.run()


if __name__ == "__main__":
    generateTrayIcon()
