from docx import Document
import asyncio
from tqdm import tqdm

HOST = "42.0.96.31"
PORT = 9999
FORMAT ="utf-8"
SIZE = 1048576

async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = None
    while True:

       #Otrzymywanie nazwy i rozmiaru pliku
       data = await reader.read(SIZE) #jak dluga ma byc wiadomosc
       data = data.decode(FORMAT)
       item = data.split("_")
       FILENAME = item[0]
       FILESIZE = int(item[1])
       print("[+] Filename and filesize received from the client.")
       writer.write("Filename and filesize received.".encode(FORMAT))

       #Otrzymywanie tresci pliku .txt
       bar = tqdm(range(FILESIZE), f"Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=SIZE)
       with open(f"recv_{FILENAME}", "w") as f:
        while True:
           data = await reader.read(SIZE) #jak dluga ma byc wiadomosc
           data = data.decode(FORMAT)
           
           if not data:
              break
           f.write(data)
           writer.write("Data received".encode(FORMAT))
           bar.update(len(data))

       await writer.drain()

       writer.close()
       await writer.wait_closed()

async def run_server()->None:
    #za kazdym razem gdy serwer otrzyma jakies dane wywolujemy handle_echo
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    async with server:
        await server.serve_forever()

def to_docx(file_path_plain_text, file_path_docx):
    
    document = Document()
    with open(file_path_plain_text) as f:
        for line in f:
            document.add_paragraph(line)
    document.save(file_path_docx)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())
    to_docx('recv_Document.txt', 'recv_Document.docx')
    input('Kliknij Enter by wyjść z programu...')

    


