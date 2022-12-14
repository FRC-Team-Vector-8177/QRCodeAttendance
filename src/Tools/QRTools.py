import qrcode
import io
import sys
import os
from os.path import exists
from PIL import Image, ImageFont, ImageDraw


# To check whether running locally or through EXE
def resource_path(relative_path, abspath):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(abspath)

    return os.path.join(base_path, relative_path)


def generate_ID_card(name, data):
    if not exists("./IDcard"):
        os.mkdir("./IDcard")

    cardBGx, cardBGy = (571, 904)
    cardBG = Image.open(resource_path('cardBG.png', './assets/card/'))
    cardFont = ImageFont.truetype(
        resource_path('Montserrat.ttf', './assets/card/'), 45)

    qr = qrcode.QRCode()
    qr.add_data(data)
    QRimg = qr.make_image(fill_color="black", back_color="white")
    QRimg = QRimg.resize((450, 450))
    cardBG.paste(QRimg, (61, 60))
    draw = ImageDraw.Draw(cardBG)
    nameArr = name.split(" ")
    current_h, pad = 525, 10
    for line in nameArr:
        w, h = cardFont.getsize(line)
        draw.text(((cardBGx-w)/2, current_h), line,
                  font=cardFont, fill="black")
        current_h += h + pad
    cardBG.save("./IDcard/" + str(data) + name.replace(" ", "_") + ".png")
