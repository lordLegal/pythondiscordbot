from typing import Sized
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageTk
from asyncio.tasks import sleep
import requests
import shutil
import time
# This is the image url.


def download(url, id_str):
    image_url = url  # "https://cdn.discordapp.com/avatars/282616377653592064/db60e7866781b77308d15b59891e26d9.webp?size=1024"
    resp = requests.get(image_url, stream=True)
    local_file = open(f'{id_str}.png', 'wb')
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp


def edit(url, usr_id_str, usr_funame, rank, lvl, xp, xp_erreichen):
    download(url, usr_id_str)
    time.sleep(2)
    font = ImageFont.truetype("font2.ttf", 30)
    font2 = ImageFont.truetype("font2.ttf", 50)

    img = Image.open("vorlage.png")
    img2 = Image.open(f"{usr_id_str}.jpg")
    img3 = Image.open("profpfp.png")
    img3.resize((29, 29), Image.ANTIALIAS)

    draw = ImageDraw.Draw(img)
    img.paste(img2, (530, 48))
    img.paste(img3, (400, 20), mask=img3)
    draw.text((0, 0), f"{usr_funame}", (240, 248, 255), font=font)
    draw.text((1080, 0), f"Rank#{rank}", (240, 248, 255), font=font)

    draw.text((565, 250), f"LVL: {lvl}", (240, 248, 255), font=font2)
    draw.text((490, 300), f"{xp}/{xp_erreichen} XP",
              (240, 248, 255), font=font2)

    img.save(f'{usr_id_str}_send.png', 'PNG')


def leaderboard(rank, link, name, xp, guild_name):
    font = ImageFont.truetype("fontlead.ttf", 100)
    font2 = ImageFont.truetype("fontlead.ttf", 80)
    img = Image.new('RGB', (2480, 3508), color='black')
    draw = ImageDraw.Draw(img)
    draw.text(
        (470, 196), f"Leaderboard from {guild_name}", (240, 248, 255), font=font)
    draw.text(
        (350, 390), f"Rank", (240, 248, 255), font=font2)
    draw.text(
        (1150, 390), f"Name", (240, 248, 255), font=font2)
    draw.text(
        (1900, 390), f"XP", (240, 248, 255), font=font2)

    rank_pos = 3508
    name_pos = 990
    xp_pos = 1890

    draw.text(
        (rank_pos, 700), f"{rank}#", (240, 248, 255), font=font2)  # +300
    draw.text(
        (name_pos, 700), f"{name}", (240, 248, 255), font=font2)  # +300
    draw.text(
        (xp_pos, 700), f"{xp}", (240, 248, 255), font=font2)  # +300

    for i in range(10):
        print(rank)
        print(i)
        plus_rank_pos = int(rank_pos + (300 * int(rank)))
        plus_name_pos = int(name_pos + (300 * int(rank)))
        plus_xp_pos = int(xp_pos + (300 * int(rank)))

        draw.text(
            (plus_rank_pos, 700), f"{rank}#", (240, 248, 255), font=font2)  # +300
        draw.text(
            (plus_name_pos, 700), f"{name}", (240, 248, 255), font=font2)  # +300
        draw.text(
            (plus_xp_pos, 700), f"{xp}", (240, 248, 255), font=font2)  # +300
        i = i+1

    pr_img = Image.open("local_image.jpg")
    img.paste(pr_img, (600, 650))  # +300

    img.save("jaj.png", "PNG")


'''
leaderboard("1", "https://cdn.discordapp.com/avatars/282616377653592064/db60e7866781b77308d15b59891e26d9.webp?size=1024",
            "Retox#5652", "255", "Python Bot")
'''

# name + #123, rank in guild, lvl in guild, current xp_str + next LVL XP str
# edit("https://cdn.discordapp.com/avatars/282616377653592064/db60e7866781b77308d15b59891e26d9.webp?size=1024",
#     "local_image", "Retox#5652", "1", "1", "3998", "4000")
