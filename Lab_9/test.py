def first_generator():
    yield 1
    yield 2

def second_generator():
    yield from first_generator() # делегирует выполнение first_generator
    yield 3

for num in second_generator():
    print(num)