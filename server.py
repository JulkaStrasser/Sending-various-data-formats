import asyncio

# HOST ="192.168.92.6"
HOST = "42.0.96.31"
PORT = 9999

async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = None
    while data != b"quit":
       data = await reader.read(1024) #jak dluga ma byc wiadomosc
       msg = data.decode()
       addr, port = writer.get_extra_info("peername")
       print(f"Wiadomosc od {addr}:{port}:{msg!r}")
       writer.write(data)
       await writer.drain()

    writer.close()
    await writer.wait_closed()

async def run_server()->None:
    #za kazdym razem gdy serwer otrzyma jakies dane wywolujemy handle_echo
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())
    input('Kliknij Enter by wyjść z programu...')
