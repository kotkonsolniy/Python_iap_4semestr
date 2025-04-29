import asyncio

async def print_numbers():
    for i in range(1, 11):
        print(i)
        await asyncio.sleep(1)

# для запуска асинхронной функции
asyncio.run(print_numbers())
