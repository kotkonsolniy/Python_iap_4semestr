import asyncio
import aiofiles #библиотека для асинхронных файловых операций


async def read_file():
    async with aiofiles.open('example.txt', mode='r') as f:
       contents = await f.read()
       print(contents)

asyncio.run(read_file())
