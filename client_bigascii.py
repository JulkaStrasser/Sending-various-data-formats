import asyncio
import time
from tqdm import tqdm
import os
from PIL import Image

ascii_characters_by_surface = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


HOST = "42.0.96.31"
# HOST ="192.168.92.6"
PORT = 9999
FORMAT = "utf-8"
SIZE = 1024
FILENAME = "image.txt"
FILESIZE = os.path.getsize(FILENAME)
IMAGENAME = "./j.jpg"

def create_ascii_art():
    image = Image.open(IMAGENAME)
    ascii_art = img_to_ascii_art(image)
    save_txt_file(ascii_art)

def img_to_ascii_art(image):
    ascii_art = []
    (width, height) = image.size
    for y in range(0, height - 1):
        line = ''
        for x in range(0, width - 1):
            px = image.getpixel((x, y))
            line += convert_pixel_to_character(px)
        ascii_art.append(line)
    return ascii_art


def convert_pixel_to_character(pixel):
    (r, g, b) = pixel
    pixel_brightness = r + g + b
    max_brightness = 255 * 3
    brightness_weight = len(ascii_characters_by_surface) / max_brightness
    index = int(pixel_brightness * brightness_weight) - 1
    return ascii_characters_by_surface[index]


def save_txt_file(ascii_art):
    with open(FILENAME, "w") as file:
        for line in ascii_art:
            file.write(line)
            file.write('\n')
        file.close()


async def run_client()->None:
    #LACZENIE Z SERWEREM
    reader, writer = await asyncio.open_connection(HOST,PORT) 

    #WYSYLANIE DO SERWERA NAZWY PLIKU I JEGO ROZMIARU
    data = f"{FILENAME}_{FILESIZE}"
    writer.write(data.encode(FORMAT))
    msg = await reader.read(SIZE) #jak dluga ma byc wiadomosc
    msg = msg.decode(FORMAT)
    print(f"SERWER: {msg}")

    #WYSYLANIE ZAWARTOSCI PLIKU
    bar = tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=SIZE)
    with open(FILENAME, "r") as f:
        while True:
            data = f.read(SIZE)

            if not data:
                await writer.drain()
                break

            writer.write(data.encode(FORMAT))
            msg = await reader.read(SIZE) #jak dluga ma byc wiadomosc
            msg = msg.decode(FORMAT)
            bar.update(len(data))


if __name__ == "__main__":
    create_ascii_art()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
    input('Kliknij Enter by wyjść z programu...')