# https://citeseerx.ist.psu.edu/doc/10.1.1.14.5908
# https://www.csd.uoc.gr/~hy460/pdf/Dynamic%20Hash%20Tables.pdf
# https://planetmath.org/goodhashtableprimes

from typing import Any
import numpy as np
# from ListaDinamica import *

MINIMUN_SIZE = 256
DIRECTORY_MAXIMUM_LENGTH = 256
SEGMENTS_MAXIMUM_LENGTH = 256
PRIME = 104883
UPPER_BOUND = 5
LOWER_BOUND = 0


class Segment:

    def __init__(self) -> None:
        self.pointer_list = [None] * SEGMENTS_MAXIMUM_LENGTH

    def __getitem__(self, i: int):
        return self.pointer_list[i]

    def __setitem__(self, i: int, value: Any):
        self.pointer_list[i] = value

    def colisions(self) -> np.ndarray:
        colision_distribuition = np.array(
            list(map(self.count_nodes, self.pointer_list)))
        return colision_distribuition

    @staticmethod
    def count_nodes(node: 'Node') -> int:
        count = 0
        while node is not None:
            count += 1
            node = node.next
        return count


class Node:
    def __init__(self, key, value: Any) -> None:
        self.value: Any = value
        self.key: str = key
        self.next: Node | None = None


class HashTable:

    def __init__(self) -> None:
        self.doubled: int = 0  # L
        self.next_bucket: int = 0  # p
        self.length: int = 0
        self.upper_bound: int = UPPER_BOUND
        self.lower_bound: int = LOWER_BOUND
        self.directory: list[Segment] = [
            Segment()] + [None] * (DIRECTORY_MAXIMUM_LENGTH - 1)
        self.maxp = MINIMUN_SIZE * 2**self.doubled
        self.keys: list[str] = []

    def __len__(self) -> int:
        return self.length

    @staticmethod
    def str2int(string: str) -> int:
        string = string.encode('ascii')
        return int.from_bytes(string, byteorder='big')

    def address(self, key: str) -> int:
        key = self.str2int(key)
        h: int = key % PRIME
        addr: int = h % self.maxp
        if addr < self.next_bucket:
            addr = h % (self.maxp * 2)
        return addr

    def find_head(self, key: str) -> Node:
        addr: int = self.address(key)
        current_segment: Segment = self.directory[addr //
                                                  SEGMENTS_MAXIMUM_LENGTH]
        segment_i: int = addr % DIRECTORY_MAXIMUM_LENGTH
        return current_segment[segment_i]

    def find(self, key: str) -> Any:
        current_node: Node = self.find_head(key)
        while current_node != None:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next

    def get_keys(self) -> list[str]:
        return self.keys

    def insert(self, key: str, value: Any) -> None:
        if self.length / self.maxp > self.upper_bound:
            self.expand_table()

        new_node: Node = Node(key, value)

        addr = self.address(key)

        current_segment: Segment = self.directory[addr //
                                                  SEGMENTS_MAXIMUM_LENGTH]
        segment_i: int = addr % DIRECTORY_MAXIMUM_LENGTH
        current_node: Node | None = current_segment[segment_i]

        if current_node == None:
            current_segment[segment_i] = new_node
        else:
            while current_node.next != None:
                current_node = current_node.next
            current_node.next = new_node

        self.keys.append(key)
        self.length += 1

    def expand_table(self) -> None:
        if self.maxp + self.next_bucket < DIRECTORY_MAXIMUM_LENGTH * SEGMENTS_MAXIMUM_LENGTH:

            new_addr: int = self.maxp + self.next_bucket

            directory_i = new_addr // SEGMENTS_MAXIMUM_LENGTH
            if new_addr % SEGMENTS_MAXIMUM_LENGTH == 0:
                self.new_segment(directory_i)

            new_segment: Segment = self.directory[directory_i]
            new_segment_i: int = new_addr % SEGMENTS_MAXIMUM_LENGTH

            old_segment: Segment = self.directory[self.next_bucket //
                                                  SEGMENTS_MAXIMUM_LENGTH]
            old_segment_i: int = self.next_bucket % SEGMENTS_MAXIMUM_LENGTH

            self.resize()

            current_n: Node = old_segment[old_segment_i]
            new_segment[new_segment_i]: Node | None = None
            previous: Node | None = None
            last_of_new: Node | None = None

            while current_n != None:

                if self.address(current_n.key) == new_addr:

                    if last_of_new == None:
                        new_segment[new_segment_i] = current_n
                    else:
                        last_of_new.next = current_n

                    if previous == None:
                        old_segment[old_segment_i] = current_n.next
                    else:
                        previous.next = current_n.next

                    last_of_new = current_n
                    current_n = current_n.next
                    last_of_new.next = None
                else:
                    previous = current_n
                    current_n = current_n.next

    def new_segment(self, i: int) -> None:
        self.directory[i] = Segment()

    def resize(self) -> None:
        self.next_bucket += 1
        if self.next_bucket == self.maxp:
            self.doubled += 1
            self.maxp = MINIMUN_SIZE * 2**self.doubled
            self.next_bucket = 0

    def remove(self, key: str) -> None:
        current_node: Node = self.find_head(key)

        if current_node is None:
            return

        if current_node.key == key:
            addr: int = self.address(key)
            current_segment: Segment = self.directory[addr //
                                                      SEGMENTS_MAXIMUM_LENGTH]
            segment_i: int = addr % DIRECTORY_MAXIMUM_LENGTH
            current_segment[segment_i] = current_node.next
        else:
            while current_node.next is not None:
                if current_node.next.key == key:
                    current_node.next = current_node.next.next
                    break
                current_node = current_node.next

        self.length -= 1
        if self.length / self.maxp < self.lower_bound:
            self.shrink_table()

    def shrink_table(self):
        raise NotImplementedError("Shrink_table not implemented")

    def shrink(self) -> None:
        self.next_bucket -= 1
        if self.next_bucket < 0:
            self.doubled -= 1
            self.maxp = MINIMUN_SIZE * 2**self.doubled
            self.next_bucket = self.maxp

    def collision_stats(self) -> dict:
        i = 0
        current_dir = self.directory[i]
        collisions_list = np.array([])  
        while current_dir is not None:
            collisions_list = np.append(
                collisions_list, current_dir.colisions())
            i += 1
            current_dir = self.directory[i]

        collisions_list = np.sort(collisions_list)
        stats = {}
        stats['median'] = np.median(collisions_list)
        stats['average'] = np.mean(collisions_list)
        stats['max'] = np.max(collisions_list)
        stats['min'] = np.min(collisions_list)

        return stats


# if __name__ == '__main__':
#     return 0
