from random import randint


async def create_conversion():
    first_num = randint(1, 10)
    second_num = randint(1, 10)
    sum_nums = first_num + second_num

    return first_num, second_num, sum_nums