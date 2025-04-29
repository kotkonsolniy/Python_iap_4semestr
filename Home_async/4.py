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

# async def main():
#     t1 = asyncio.create_task(task1())
#     t2 = asyncio.create_task(task2())
#     t3 = asyncio.create_task(task3())
#     await t1  # Можно ждать выборочно
#     await t2
#     await t3

# Запуск всех задач
asyncio.run(main())
