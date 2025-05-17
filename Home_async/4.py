import asyncio

async def task1():
    await asyncio.sleep(1)
    print("Первая задача завершена")

async def task2():
    await asyncio.sleep(2)
    print("Вторая задача завершена")

async def task3():
    await asyncio.sleep(3)
    print("Третья задача завершена")

async def main():
    await asyncio.gather(
        task1(),
        task2(),
        task3()
    )

# async def main():
#     # Запуск всех задач параллельно
#     await asyncio.gather(task1(), task2(), task3())


# Запуск всех задач
asyncio.run(main())
