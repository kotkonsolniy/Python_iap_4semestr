import asyncio


async def check_ports(port):
        try:
            await asyncio.open_connection('127.0.0.1', port)
            print(f'Доступный порт: {port}')
        except Exception as e:
            pass


async def main():
    tasks = [check_ports(port) for port in range(1, 65535)]
    await asyncio.gather(*tasks) #параллельное выполнение

asyncio.run(main())
