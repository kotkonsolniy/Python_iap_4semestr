#асинхронный
import asyncio #длля асинхроннорго выполнения
import time #для замера временни
import aiohttp #асинхронный аналог requests

async def main():
    sites = [
        "https://www.yandex.ru",
        "https://bmstu.ru",
    ] * 800
    start_time = time.perf_counter()
    await download_all_sites(sites) #запуск асинхронной загрузки
    duration = time.perf_counter() - start_time
    print(f"Dowload {len(sites)} sites in {duration} seconds")



async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session: #асинхронный аналог request экономит ресурсы
        tasks = [download_site(url, session) for url in sites] # список корутин(асинх задач) для каждого url
        await asyncio.gather(*tasks, return_exceptions=True) #запуск всех задач конкурентно (не бокируя друг друга)

#функция загрузки одной страницы
async def download_site(url, session):
    async with session.get(url) as response: #yне блокирует поток пока ждет ответа
        print(f"Read {len(await response.read())} bytes from {url}") #асинхронно читает содержимое страницы

if __name__ == "__main__":
    asyncio.run(main()) #точка входа в асинхронный код