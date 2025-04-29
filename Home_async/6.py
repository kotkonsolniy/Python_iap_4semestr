import asyncio
import aiohttp

sites = [
    'https://www.google.com',
    'https://www.github.com',
    'https://www.python.org',
    'https://www.kali.org',
]

async def ping_site(session, url):
    try:
        async with session.get(url, timeout=5) as response:
            print(f'{url} -> {response.status}')
    except Exception as e:
        print(f'{url} -> Error: {e}')


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [ping_site(session, url) for url in sites]
        await asyncio.gather(*tasks) #запуск задач одновременно

asyncio.run(main())