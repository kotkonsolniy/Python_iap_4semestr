import asyncio


# Пример асинхронной функции z(x)
async def z(x):
    await asyncio.sleep(1)
    return x * 2


# Пример асинхронного генератора gen(x)
async def gen(x):
    for i in range(x):
        await asyncio.sleep(0.1)
        yield i


# 1. Обычная корутина
async def f(x):
    y = await z(x)
    return y


# 2. Асинхронный генератор
async def g(x):
    yield x


# 3. Аналог yield from для асинхронного генератора
async def m(x):
    async for item in gen(x):
        yield item


# 4. Исправленный await
async def n(x):
    y = await z(x)
    return y


# Тестируем
async def main():
    print(await f(5))  # 10 (5 * 2)

    async for num in g(3):
        print(num)  # 3

    async for num in m(4):
        print(num)  # 0, 1, 2, 3

    print(await n(10))  # 20 (10 * 2)


asyncio.run(main())