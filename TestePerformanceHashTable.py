import unittest
# from HashTable import * 
from HashTable2 import * 
from random import randint, choice
from config import *
from TesteFuncUtils import *

class TestePerfomanceHashTable(unittest.TestCase):
    
    def setUp(self) -> None:
        self.hash_table = HashTable()
        for _ in range(AMOUNT_OF_TST_CASES):
            self.hash_table.insert(make_rand_str(LENGTH_RAND_STR), randint(0, 10))
        self.keys = self.hash_table.get_keys()

    @time_it
    def test_insert_speed(self):
        self.hash_teste = HashTable()
        for _ in range(AMOUNT_OF_TST_CASES):
            self.hash_teste.insert(make_rand_str(LENGTH_RAND_STR), randint(0, 10))

    @time_it
    def test_find_speed(self):
        for _ in range(AMOUNT_OF_TST_CASES):
            self.hash_table.find(choice(self.keys))

    @time_it
    def test_remove_speed(self):
        for key in self.hash_table.get_keys():
            self.hash_table.remove(key)             
    
    @time_it
    def test_hash_time(self):
        for _ in range(AMOUNT_OF_TST_CASES):
            self.hash_table.address(make_rand_str(LENGTH_RAND_STR))
    
    # def test_collision(self):
    #     stats = self.hash_table.collision_stats()

    #     print(stats)  


if __name__ == '__main__':
    unittest.main()