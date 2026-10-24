import os
import socket
import textwrap
from datetime import datetime
from importlib.resources import files
from io import BytesIO

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageOps
from zebrafy.zebrafy_image import ZebrafyImage

from .weather import fetch


def main() -> None:
    print("Gathering Label Information")
    load_dotenv()
    xcoord = float(os.environ.get("XCOORD") or 27.9881)  # if no coords are provided, you're going to everest
    ycoord = float(os.environ.get("YCOORD") or 86.9250)

    weather = fetch(xcoord, ycoord)
    print(weather)
    print("Formatting Label")

    # Geneerate the Header text

    # just some sensible defaults
    height = float(os.environ.get("HEIGHT") or 6)
    width = float(os.environ.get("WIDTH") or 4)
    dpi = int(os.environ.get("DPI") or 300)

    image = Image.new("L", (int(width * dpi), int(height * dpi)), "white")

    draw = ImageDraw.ImageDraw(image)

    # import the font
    fontfilename = os.environ.get("FONT_FILENAME") or "OpenSans-Regular.ttf"
    fontfile = files(__package__) / "assets" / "fonts" / fontfilename  # pyright: ignore[reportArgumentType]

    if not fontfile:
        raise FileNotFoundError(f"Did not find font file at assets/fonts/{fontfilename}")

    with fontfile.open("rb") as f:
        font = ImageFont.truetype(f, dpi // 5)  # pyright: ignore[reportArgumentType]

    with fontfile.open("rb") as f:
        font_small = ImageFont.truetype(f, dpi // 8)  # pyright: ignore[reportArgumentType]

    readabledate = datetime.now().strftime("%A, %B %d, %Y")

    header = f"""
Report for {readabledate}
Weather is {weather.weather_text}
{"Precipitation is " + str(weather.precipitation) if weather.precipitation > 0 else "No precipitation expected today"}
Highs of {weather.maxtemp:.1f} with lows of {weather.mintemp:.1f}

"""

    draw.text((10, 10), header, fill="black", font=font)

    # Get cat photo
    # https://cataas.com/cat/says/bottom text?type=square&fontSize=10
    catimg = None
    catres = requests.get("https://cataas.com/cat?type=square")
    if catres.status_code == 200:
        catimg = Image.open(BytesIO(catres.content))

    # catimg.save("catimg.png") # uncomment this if you need more cat images

    # print("cat image stats:", catimg.size) #all square cat images from cataas are 200 x 200

    catimg = ImageOps.scale(catimg, factor=5)

    image.paste(catimg, (100, 400))

    quoteres = requests.get("https://dummyjson.com/quotes/random")
    if quoteres.status_code == 200:
        quotejson = quoteres.json()
        footer = textwrap.fill(quotejson["quote"], 53) + "\n\n" + "  - " + quotejson["author"]

        draw.text((100, 1400), footer, fill="black", font=font_small)

    print("Printing Label")

    zpl = ZebrafyImage(image=image, dither=True, format="Z64")

    ip = os.environ.get("PRINTER_IP")
    port = os.environ.get("PRINTER_PORT")

    dry_run = os.environ.get("DRY_RUN") != "FALSE"

    if dry_run:
        # for testing, makes it easy to see when developing on a remote machine, image.show() doesn't work
        image.save("label.png")
    else:
        with socket.create_connection((ip, port)) as s:
            s.sendall(zpl.to_zpl().encode())

    print("Done")
