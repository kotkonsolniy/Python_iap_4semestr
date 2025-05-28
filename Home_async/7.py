#на долеать
import asyncio

async def timer():
    try:
        while True:
            print("хоба на...") #каждую секунду выводит
            await asyncio.sleep(1)
    except asyncio.CancelledError: #
        print("Таймер остановлен")

async def main():
    task = asyncio.create_task(timer())  # запуск таймиера как отдельной задачи
    await asyncio.sleep(5)               #ждет 5 секунд
    task.cancel()                        # отмена таймера
    try:
        await task                       # Ожидаем завершения с учётом отмены
    except asyncio.CancelledError:       #ллловит исключение если таймер его не обрабатывает
        pass

asyncio.run(main())
