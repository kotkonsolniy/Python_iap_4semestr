import asyncio
import  aiohttp

async def func():
    url = 'https://httpbin.org/get'
    async with aiohttp.ClientSession() as session: #создание сессиии http запросов
        async with session.get(url) as response: #отправление get запроса
            a = await response.text()
            print(a)

asyncio.run(func())
