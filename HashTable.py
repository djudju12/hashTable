# https://citeseerx.ist.psu.edu/doc/10.1.1.14.5908
# https://www.csd.uoc.gr/~hy460/pdf/Dynamic%20Hash%20Tables.pdf

from typing import Any
from ListaDinamica import *
import numpy as np

INITIAL_CAPATY = 500
PRIME = 104883

class NodeHash:
    def __init__(self, key: str, valor: Any) -> None:
        self.value: Any = valor 
        self.key: str = key 

    def __eq__(self, other: 'NodeHash') -> bool:
        if isinstance(other, NodeHash):
            return (other.value == self.value and other.key == self.key)
        return False

# class Nodes: 
#     def __init__(self, node: NodeHash) -> None:
#         self.list: ListaEncadeada = ListaEncadeada()
#         self.list.append(node)


class HashTable:
    def __init__(self) -> None:
        self.capacity: int = INITIAL_CAPATY
        self.keys: list[str] = []  
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

    # def print_hash(self) -> None:
    #     print("{ ", end="")
    #     for nodes in self.buckets:
    #         if nodes is not None:
    #             for node in nodes.list:
    #                 print(f"'{node.key}' -> {node.value}", end=" ")
    #     print("}", end="")

    def insert(self, key, value) -> None:
        self.size += 1 
        index: int = self.address(key)
        # nodes: Nodes = self.buckets[index]
        nodes: ListaEncadeada = self.buckets[index]
        node: NodeHash = NodeHash(key, value)
        self.keys.append(key)

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
                nodes.first_ocurrence(node)
                self.size -= 1 


if __name__ == '__main__':
    hash1 = HashTable()
    from TesteFuncUtils import make_rand_str
    from time import time
    strs = [make_rand_str(10) for n in range(100000)]
    ini = time()
    for n in range(100000):
        hash1.insert(strs[n], 10)

    # for n in range(1000):
    #     hash1.find(strs[n])
    
    # for n in range(1000):
    #     hash1.remove(strs[n])

    print( hash1.stats())
        

