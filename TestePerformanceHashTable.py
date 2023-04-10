# DESCOMENTE a hashtable que voce quer testar. 

from HashTable import * 
# from HashTableDinamica import *

# Lembre-se que o teste EXPAND deve ser comentado
# para a hash table estatica

from configTestes import *
from TesteFuncUtils import *
from layoutTestes import str_layout
VALUES = []

class TestePerfomanceHashTable:
    """
    Testes simples de insercao, remocao, procura e hashing.
    
    Stats retorna as estatisticas de colisao.
    """

    def __init__(self) -> None:
        self.hash_table: HashTable = None
        self.random_strs = [make_rand_str(LENGTH_RAND_STR)
                            for _ in range(AMOUNT_OF_TST_CASES)]

    @time_it
    def insert(self):
        self.hash_table = HashTable()
        for n in range(AMOUNT_OF_TST_CASES):
            self.hash_table.insert(self.random_strs[n], 20)

    def stats(self):
        return self.hash_table.stats()

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
    VALUES.append(teste.insert())
    print(teste.stats()) # Printe os stats antes de remover os itens da hash table 
    VALUES.append(teste.find())
    VALUES.append(teste.remove())
    VALUES.append(teste.hash())
    print(str_layout(VALUES))
