import asyncio
import time

# HOST ="192.168.92.6"
HOST = "42.0.96.31"
PORT = 9999


async def run_client()->None:
    reader, writer = await asyncio.open_connection(HOST,PORT) #LACZENIE Z SERWEREM

    writer.write(b"Hello world!")
    await writer.drain()
    no_messages = 10

    while True:
        data = await reader.read(1024)

        if not data:
            raise Exception("serwer nie chce z toba rozmawaiac")
        print(f"Received:{data.decode()!r}")

        if no_messages>0:
            await asyncio.sleep(1)
            writer.write(b"Hello world!")
            await writer.drain()
            no_messages -= 1
        else:
            writer.write(b"quit")
            await writer.drain()
            break

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())
    input('Kliknij Enter by wyjść z programu...')