import docx2txt
import glob
import asyncio
import time
from tqdm import tqdm
import os

HOST = "42.0.96.31"
PORT = 9999
FORMAT = "utf-8"
SIZE = 1048576
FILENAME = "Document.txt"
FILESIZE = os.path.getsize(FILENAME)

async def run_client()->None:
    reader, writer = await asyncio.open_connection(HOST,PORT) #LACZENIE Z SERWEREM

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


def convert_docx():
    directory = glob.glob('./Document.docx')

    for file_name in directory:

        with open(file_name, 'rb') as infile:
            outfile = open(file_name[:-5]+'.txt', 'w', encoding='utf-8')
            doc = docx2txt.process(infile)

            outfile.write(doc)

        outfile.close()
        infile.close()

if __name__ == "__main__":
    convert_docx()
    print('Skonwertowano plik Document.docx')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
    input('Kliknij Enter by wyjść z programu...')
    
   