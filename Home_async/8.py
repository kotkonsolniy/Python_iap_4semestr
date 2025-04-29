import asyncio

async def async_input(prompt: str = "") -> str: #делаем так чтобы инпут не блокировал поток
    loop = asyncio.get_event_loop() #поллучение текущего цикла событий
    return await loop.run_in_executor(None, input, prompt) #запуск инпута в отдельном потоке

async def handle_input():
    while True:
        user_input = await async_input("Введите команду или exit: ")
        if user_input.lower() == "exit":
            print("Программа завершена.")
            break
        else:
            print(f"Вы ввели: {user_input}")

asyncio.run(handle_input())

