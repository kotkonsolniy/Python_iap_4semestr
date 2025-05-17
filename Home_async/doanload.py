import asyncio
import aiohttp
import aiofiles

CHUNK_SIZE = 8192  # размер буфера (8 КБ)

async def write_file(file, resp):
    async with aiofiles.open(file, mode='wb') as f:
        async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
            if chunk:
                await f.write(chunk)

async def get_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                filename = url.split('/')[-1]
                await write_file(file=filename, resp=resp)
            else:
                print(f"Ошибка {resp.status} при скачивании {url}")

async def main():
    hosts = [
        #
        "https://masterpiecer-images.s3.yandex.net/5fd531dca6427c7:upscaled"
    ]
    tasks = [get_url(host) for host in hosts]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
