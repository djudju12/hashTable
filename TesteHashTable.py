# DESCOMENTE a hashtable que voce quer testar. 

from HashTable import * 
# from HashTableDinamica import *

# Lembre-se que o teste EXPAND deve ser comentado
# para a hash table estatica


import unittest
from configTestes import *
from TesteFuncUtils import make_rand_str # Gera uma string aleatoria como key

class TesteHashTable(unittest.TestCase):
    """
    Testes simples de insercao, remocao, procura e tamanho.

    O teste de expansao eh feito apenas para a dinamica: "Asserta" que foi alocado
    um novo segmento para a hashtable. 

    Rode o arquivo para visualizar os testes.
    """
    def setUp(self):
        self.hash_table = HashTable()
        self.hash_table.insert("apple", 5)
        self.hash_table.insert("orange", 50)
        self.hash_table.insert("batata", 10)

    def test_insert(self):
        self.hash_table.insert("dog", 7)
        self.assertEqual(self.hash_table.find("dog"), 7)

    def test_remove(self):
        self.hash_table.remove("apple")
        self.assertIsNone(self.hash_table.find("apple"))
        self.assertEqual(self.hash_table.find("orange"), 50)
        self.hash_table.insert("teste", 20)
        self.hash_table.remove("teste")
        self.assertIsNone(self.hash_table.find("teste"))

    def test_resize_len(self):
        len1 = len(self.hash_table)
        self.hash_table.insert("papel", 3)
        len2 = len(self.hash_table)
        self.assertEqual(len1+1, len2)
        self.hash_table.remove("papel")
        self.assertEqual(len2-1, len(self.hash_table))

    def test_find(self):
        value = self.hash_table.find("batata")
        self.hash_table.insert("teste123", 123)
        self.assertEqual(self.hash_table.find("teste123"), 123)
        self.assertEqual(value, 10)

    # def test_expand(self):
    #     """
    #     Esse teste só pode ser feito na Hash Table dinamica. Comente-o para 
    #     a estatica
    #     """
    #     self.assertIsNone(self.hash_table.directory[1])
    #     for _ in range(SEGMENTS_MAXIMUM_LENGTH*(UPPER_BOUND + 1)):
    #         self.hash_table.insert(make_rand_str(LENGTH_RAND_STR), 1)
    #     self.assertEqual(self.hash_table.doubled, 1)
    #     self.assertIsNotNone(self.hash_table.directory[1])
    #     self.assertTrue(any(self.hash_table.directory[1]))

        
if __name__ == '__main__':
    unittest.main()    

