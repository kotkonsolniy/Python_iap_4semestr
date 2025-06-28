def count_up_to(n):
    i = 1
    while i <+ n:
        yield i #возвращает i и приостанавливает выполнение
        i += 1


gen = count_up_to(3)

print(gen, type(gen))

# print(next(gen))
# print(next(gen))
# print(next(gen))

# for num in count_up_to(5):
#     print(num)

# gen_obj = count_up_to(5)
#
# for num in gen_obj:
#     print(num)
#
# for num in gen_obj:
#     print(num)

range_obj = range(1, 5000)

# print(range_obj, type(range_obj))

print(next(range_obj))