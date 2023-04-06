import unittest
from config import *
from HashTable2 import * 
from config import *
from TesteFuncUtils import make_rand_str

class TesteHashTable(unittest.TestCase):
    def setUp(self):
        self.hash_table = HashTable()
        self.hash_table.insert("apple", 5)
        self.hash_table.insert("orange", 50)
        self.hash_table.insert("batata", 10)

    def test_insert(self):
        self.hash_table.insert("dog", 7)
        self.assertEqual(self.hash_table.find("dog"), 7)
        print("Insert OK")

    def test_remove(self):
        self.hash_table.remove("apple")
        self.assertIsNone(self.hash_table.find("apple"))
        self.assertEqual(self.hash_table.find("orange"), 50)
        self.hash_table.insert("teste", 20)
        self.hash_table.remove("teste")
        self.assertIsNone(self.hash_table.find("teste"))
        print("Delete OK")

    def test_resize_len(self):
        len1 = len(self.hash_table)
        self.hash_table.insert("papel", 3)
        len2 = len(self.hash_table)
        self.assertEqual(len1+1, len2)
        self.hash_table.remove("papel")
        self.assertEqual(len2-1, len(self.hash_table))
        print("Resize length OK")

    def test_find(self):
        value = self.hash_table.find("batata")
        self.hash_table.insert("teste123", 123)
        self.assertEqual(self.hash_table.find("teste123"), 123)
        self.assertEqual(value, 10)
        print("Find OK")
    
    def test_get_keys(self):
        self.assertTrue("batata" in self.hash_table.get_keys())
        print("Get keys OK")

    def test_expand(self):
        self.assertIsNone(self.hash_table.directory[1])
        for _ in range(SEGMENTS_MAXIMUM_LENGTH*(UPPER_BOUND + 1)):
            self.hash_table.insert(make_rand_str(LENGTH_RAND_STR), 1)
        self.assertEqual(self.hash_table.doubled, 1)
        self.assertIsNotNone(self.hash_table.directory[1])
        self.assertTrue(any(self.hash_table.directory[1]))
        print("Expand OK")

    # def teste_shrink(self):
    #     for _ in range(SEGMENTS_MAXIMUM_LENGTH*(UPPER_BOUND + 1)):
    #         self.hash_table.insert(make_rand_str(LENGTH_RAND_STR), 1)
    #     keys = self.hash_table.get_keys()

    #     for key in keys:
    #         self.hash_table.remove(key)

    #     self.assertEqual(self.hash_table.doubled, 0)

if __name__ == '__main__':
    unittest.main()    

