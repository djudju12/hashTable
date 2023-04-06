from functools import wraps
from random import choice
from string import ascii_letters
from config import *
from timeit import timeit

def make_rand_str(length):
    return ''.join(choice(ascii_letters) for _ in range(length))

def time_it(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        t = timeit(lambda: func(*args, **kwargs), number=AMOUNT_OF_TST_CASES)
        print(f'Func => {func.__name__}\nNumber of execs => {AMOUNT_OF_EXECS}\nTime => {t} seconds\nExec/s => {AMOUNT_OF_EXECS/t:.4f}\nFor {AMOUNT_OF_TST_CASES} cases')
        print()
        return 
    return timeit_wrapper
