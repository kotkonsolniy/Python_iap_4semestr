import asyncio
import aiohttp
import aiofiles


#функция принимает имя файла и объект http
async def write_file(file, resp):
    f = await aiofiles.open(f'{file}', mode='wb') #асинхронно открываем файл для записи в бинарном режиме
    await f.write(await resp.read()) #асинхронно читаем ответ и записываем в файл
    await f.close() #закрываем файл


#имя файла берется из последней части url
async def get_url(url):
    async with aiohttp.ClientSession() as session: #создаем http сессию
        async with session.get(url) as resp: #выполнеям get-запрос
            if resp.status == 200: #если ответ успешный
                await write_file(file=url.split('/')[-1], resp=resp) #сохраняем файл


#
async def main():
    hosts = ["https://cdn.lifehacker.ru/wp-content/uploads/2021/03/fedora-32-workstation-default-so_1614664423.jpg"]
    tasks = [get_url(host) for host in hosts] #создает список корутин
    results = await asyncio.gather(*tasks) #запускаем все задачи параллелльно


if __name__ == '__main__':
    asyncio.run(main())
