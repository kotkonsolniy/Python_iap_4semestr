import asyncio
import aiofiles

async def write_file():
        async with aiofiles.open('output.txt', mode='w') as f:
            await f.write("Hello, async IO!")

asyncio.run(write_file())
