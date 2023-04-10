# from HashTable import *
from HashTable2 import *
from random import randint, choice
from config import *
from TesteFuncUtils import *
from layout import str_layout
VALUES = []
class TestePerfomanceHashTable:

    def __init__(self) -> None:
        self.hash_table = HashTable()
        self.random_strs = [make_rand_str(LENGTH_RAND_STR)
                            for _ in range(AMOUNT_OF_TST_CASES)]

    @time_it
    def insert(self):
        self.hash_teste = HashTable()
        for n in range(AMOUNT_OF_TST_CASES):
            self.hash_teste.insert(self.random_strs[n], randint(0, 10))

    @time_it
    def find(self):
        for n in range(AMOUNT_OF_TST_CASES):
            self.hash_table.find(self.random_strs[n])

    @time_it
    def remove(self):
        for n in range(AMOUNT_OF_TST_CASES):
            self.hash_table.remove(self.random_strs[n])

    @time_it
    def hash(self):
        for n in range(AMOUNT_OF_TST_CASES):
            self.hash_table.address(self.random_strs[n])


if __name__ == '__main__':
    teste = TestePerfomanceHashTable()
    teste.__init__()
    VALUES.append(teste.insert())
    VALUES.append(teste.find())
    VALUES.append(teste.remove())
    VALUES.append(teste.hash())
    print(str_layout(VALUES))