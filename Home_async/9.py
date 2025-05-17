import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Клиент подключён: {addr}")

    try:
        while data := await reader.readline():
            message = data.decode().strip()
            print(f"От {addr}: {message}")
            writer.write(f"Echo: {message}\n".encode())
            await writer.drain()
    finally:
        print(f"Клиент отключён: {addr}")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8889)
    print(f"Сервер запущен на {server.sockets[0].getsockname()}")

    async with server:
        await server.serve_forever()

asyncio.run(main())
