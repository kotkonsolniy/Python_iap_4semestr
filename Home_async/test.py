import asyncio
import aiohttp
import aiofiles


async def write_file(file, resp):
    f = await aiofiles.open(f'{file}', mode='wb')
    await f.write(await resp.read())
    await f.close()


async def get_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                await write_file(file=url.split('/')[-1], resp=resp)


async def main():
    hosts = ["https://masterpiecer-images.s3.yandex.net/5fd531dca6427c7:upscaled"]
    tasks = [get_url(host) for host in hosts]
    results = await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
