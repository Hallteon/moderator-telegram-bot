import random


async def create_captcha():
    modes = ["+", "-"]

    mode = random.choice(modes)
    first_num = random.randint(1, 10)
    second_num = random.randint(1, 10)
    sum_nums = 0

    if mode == "+":
        sum_nums = first_num + second_num

    elif mode == "-":
        sum_nums = first_num - second_num

    return mode, first_num, second_num, sum_nums