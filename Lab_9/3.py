def flatten(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item) # рекурсивное расплющивание списка
        else:
            yield item

nested_list = [1, [2, [3, 4], 5]]
print(list(flatten(nested_list)))
