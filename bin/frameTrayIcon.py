from PIL import Image, ImageDraw
import pystray

icon = pystray.Icon('test name')
width = 20
height = 20
color1 = "red"
color2 = "blue"


def on_clicked():
    icon.stop()


def create_image():
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


icon.icon = create_image()
icon.menu = pystray.Menu(pystray.MenuItem(
    'Close',
    on_clicked))
icon.run()
