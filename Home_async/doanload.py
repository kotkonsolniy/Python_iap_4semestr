import asyncio
import aiohttp
import aiofiles

CHUNK_SIZE = 8192  # размер буфера (8 КБ) кусочки

#запись файла по кусочкам
async def write_file(file, resp):
    async with aiofiles.open(file, mode='wb') as f: #открываем файл
        async for chunk in resp.content.iter_chunked(CHUNK_SIZE): #читаем ответ по кусочкам
            if chunk: #если чанк не пустой
                await f.write(chunk) #записываем его в файл

#обработка url
async def get_url(url):
    async with aiohttp.ClientSession() as session: #создаем сессию
        async with session.get(url) as resp: #отправляем гет запрос
            if resp.status == 200: #если ответ успешный
                filename = url.split('/')[-1] #имя файла -- последняя часть юрла
                await write_file(file=filename, resp=resp) #запись в файл
            else:
                print(f"Ошибка {resp.status} при скачивании {url}") #бработка ошибок

#запуск задачки
async def main():
    hosts = [
        #
        "https://cdn.lifehacker.ru/wp-content/uploads/2021/03/fedora-32-workstation-default-so_1614664423.jpg",
        "https://masterpiecer-images.s3.yandex.net/5fd531dca6427c7:upscaled",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQL9g041VTW-WprVhA_uCg12_6TCin0hDeEBA&s"
    ]
    tasks = [get_url(host) for host in hosts] #создание задачи
    await asyncio.gather(*tasks) #запуск задач параллеьно

if __name__ == '__main__':
    asyncio.run(main())

