import json
import qrcode
import io
import sys
import os
from PIL import Image, ImageFont, ImageDraw
from colorama import init
from os.path import exists
from datetime import date


def resource_path(relative_path):  # To check whether running locally or through EXE
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./cardsrc")

    return os.path.join(base_path, relative_path)


init()

pathToJSON = "./data.json"

cardBGx, cardBGy = (571, 904)
cardBG = Image.open(resource_path('cardBG.png'))
cardFont = ImageFont.truetype(resource_path('Montserrat.ttf'), 45)

dateString = date.today().strftime("%m-%d-%Y")


if not exists(pathToJSON):
    f = open(pathToJSON, "a")
    f.write("{\"members\":[],\"member-count\": 0}")
    f.close()

if not exists("./IDcard"):
    os.mkdir("./IDcard")


def read_json(filename=pathToJSON):
    with open(filename,) as file:
        return json.load(file)


def write_json(new_data, filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["members"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def increment_member_count(inc, filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["member-count"] = file_data["member-count"]+inc
        file.seek(0)
        json.dump(file_data, file, indent=4)


def remove_member(name, filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for i in range(len(file_data["members"])):
            if file_data["members"][i]["name"] == name:
                del file_data["members"][i]
                file_data["member-count"] -= 1
                break
        file.seek(0)
        updatedJSON = json.dumps(file_data, indent=4)
    with open(filename, 'w') as file:
        file.write(updatedJSON)
        file.close()


def print_QR_code(data, name):
    # Generate QR Code
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)

    # Generate ID card
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

    # Print QR To Console
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print('\033[0;30;47m ' + f.read() + ' \033[0;0m')


while True:
    task = input(
        "What would you like to do? Type 'add' to add a member, 'delete' to remove a member, 'get qr' to get a member's QR code, or 'quit' to quit!")
    if task == "add":
        name = input("What's the name of the user you'd like to add?")
        gradYear = input("What's the graduating year of the user?")
        if len(gradYear) > 2:
            gradYear[-2:]

        avalID = "00"
        jsonData = read_json()
        if len(jsonData["members"]) > 0:
            lastMemberID = str(
                jsonData["members"][len(jsonData["members"])-1]["id"])[-2:]
            avalID = str((int(lastMemberID) + 1)).zfill(2)
        idnum = int(gradYear + avalID)
        write_json({"id": idnum,
                    "name": name,
                    "days-attended": {

                    }}
                   )
        increment_member_count(1)
        print("Successfully added " + name +
              " as ID #" + str(idnum) + ". \nQR code:")
        print_QR_code(idnum, name)
    elif task == "delete":
        name = input("Please type the member's full name")
        remove_member(name)

    elif task == "get qr":
        name = input("Please type the member's full name")
        memberJSON = read_json()
        for member in memberJSON["members"]:
            if member["name"] == name:
                print_QR_code(member["id"], member["name"])
    elif task == "quit":
        break
    else:
        print("Invalid Input")