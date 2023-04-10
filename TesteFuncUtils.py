from functools import wraps
from random import choice
from string import ascii_letters
from configTestes import *
from timeit import timeit

def make_rand_str(length) -> str:
    """
    Gera uma string aleatorio. Usada para gerar as chaves dos testes
    """
    return ''.join(choice(ascii_letters) for _ in range(length))

def time_it(func):
    """
    decorador simples que retorna informacoes do tempo de execucao da funcao
    "func"
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        t = timeit(lambda: func(*args, **kwargs), number=AMOUNT_OF_EXECS)
        return [func.__name__, f'{AMOUNT_OF_EXECS}', f'{AMOUNT_OF_TST_CASES}', f'{t:f}']
    return timeit_wrapper
