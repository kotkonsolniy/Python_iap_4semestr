import asyncio

async def timer():
    try:
        while True:
            print("БАМ...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Таймер остановлен")

async def main():
    task = asyncio.create_task(timer())  # запуск тиаймиера как отдельной задачи
    await asyncio.sleep(5)
    task.cancel()                        # отмена таймера
    try:
        await task                       # Ожидаем завершения с учётом отмены
    except asyncio.CancelledError:
        pass

asyncio.run(main())
