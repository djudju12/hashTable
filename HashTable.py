# Static Hash Table
# Ultima Atualizacao: 10/04/2023

# Referenciais 
# https://citeseerx.ist.psu.edu/doc/10.1.1.14.5908
# https://www.csd.uoc.gr/~hy460/pdf/Dynamic%20Hash%20Tables.pdf

from typing import Any
from ListaDinamica import *
import numpy as np

INITIAL_CAPACITY = 500
PRIME = 104883

class NodeHash:
    """
    Estrutura do Nodo que compõe
    """
    def __init__(self, key: str, valor: Any) -> None:
        self.value: Any = valor 
        self.key: str = key 

    # Implementei "==" para facilitar na remocao
    def __eq__(self, other: 'NodeHash') -> bool:
        if isinstance(other, NodeHash):
            return (other.value == self.value and other.key == self.key)
        return False

class HashTable:
    """
    Hash Table estaticamente alocada. A capacidade eh dada pela variavel
    INITIAL_CAPACITY.

    Eh simplesmente um array de listas linkadas. O hash eh calculado a partir
    de um numero primo grande, dado pela variavel PRIME.
    """
    def __init__(self) -> None:
        self.capacity: int = INITIAL_CAPACITY
        self.size: int = 0 
        self.buckets: list[ListaEncadeada] = [None] * self.capacity

    def __len__(self) -> int:
        return self.size
    
    def stats(self):
        arr = np.array([])
        for bucket in self.buckets:
            if bucket is not None:
                arr = np.append(arr, len(bucket))
        
        arr = np.sort(arr)
        stats = {}

        stats['median'] = np.median(arr)
        stats['average'] = np.mean(arr)
        stats['max'] = np.max(arr)
        stats['min'] = np.min(arr)
        return stats
    
    @staticmethod
    def str2int(string: str) -> int:
        """
        Funcao auxiliar para converter uma string para inteiro
        """
        string = string.encode('ascii')
        return int.from_bytes(string, byteorder='big')

    def address(self, key) -> int:
        key = self.str2int(key)
        h: int = key % PRIME
        addr: int = h % self.capacity
        return addr

    # def address(self, key) -> int:
    #     hashsum: int = 0
    #     for idx, c in enumerate(key):
    #         hashsum += (idx + len(key)) ** ord(c)
    #         hashsum = hashsum % self.capacity 
    #     return hashsum

    def insert(self, key, value) -> None:
        """
        Inserta um novo Nodo se o valor do BUCKET for NONE. 
        Senao, simplesmente insere no fim do BUCKET.
        """
        self.size += 1 
        index: int = self.address(key)
        nodes: ListaEncadeada = self.buckets[index]
        node: NodeHash = NodeHash(key, value)
        if nodes is None:
            new_bucket = ListaEncadeada()
            new_bucket.append(node)
            self.buckets[index] = new_bucket
        else:
            nodes.append(node)

    def find(self, key) -> Any:
        index: int = self.address(key)
        nodes: ListaEncadeada = self.buckets[index]

        if nodes is None:
            return None 
        
        for node in nodes:
            if node.key == key:
                return node.value  
        
    def remove(self, key) -> None:
        index: int = self.address(key)
        nodes: ListaEncadeada = self.buckets[index]
        
        if nodes is None: 
            return None 

        for node in nodes:
            if node.key == key:
                # first_ocurrence eh uma funcao da ListaEncadeada que 
                # deleta o primeiro elemento que possuir o valor do parametro
                nodes.first_ocurrence(node)
                self.size -= 1 


if __name__ == '__main__':
    hash1 = HashTable()
    from TesteFuncUtils import make_rand_str
    from time import time
    strs = [make_rand_str(10) for _ in range(100000)]
    ini = time()
    for n in range(100000):
        hash1.insert(strs[n], 10)

    print( hash1.stats())
        

