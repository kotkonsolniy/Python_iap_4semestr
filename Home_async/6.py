#на доделать
import asyncio
import aioping

sites = [
    'google.com',
    'github.com',
    'python.org',
    'kali.org',
]

async def ping_site(host):
    try:
        delay = await aioping.ping(host, timeout=2)  # отправляет icmp запрос ожидая 2 сек
        print(f"{host} -> Ping OK: {delay * 1000:.2f} ms") #возвращает время задержки
    except TimeoutError:
        print(f"{host} -> Ping Timeout")  #если нет ответа
    except Exception as e:
        print(f"{host} -> Error: {e}") #другие ошибки

async def main():
    tasks = [ping_site(site) for site in sites]
    await asyncio.gather(*tasks) #параллельное выполнение

asyncio.run(main())
