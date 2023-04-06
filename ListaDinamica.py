from typing import Any


class Node:

    def __init__(self, value) -> None:
        self.value: tuple = value
        self.proximo: Node | None = None 

class ListaEncadeada:
    def __init__(self) -> None:
        self.primeiro: Node | None = None
        self.len: int = 0
        self.current: Node | None = self.primeiro
        self.tail: Node | None = None

    def __iter__(self) -> 'ListaEncadeada':
        self.current = self.primeiro
        return self

    def __next__(self) -> Node:
        if self.current is None:
            raise StopIteration
        else:
            no_atual = self.current
            self.current = self.current.proximo
            return no_atual.value

    def __len__(self):
        return self.len

    def __delitem__(self, index: int) -> None:
        if self.lista_vazia() or index > self.len-1:
            return print('Index fora dos limites da lista')
        elif index == 0:
            self.primeiro = self.primeiro.proximo
        else:
            count = 0
            item = self.primeiro
            for _ in self:
                if count == index-1:
                    item.proximo = item.proximo.proximo
                    if index == self.len-1:
                        self.tail = item
                    break
                item = item.proximo
                count += 1
        self.len -= 1

    def __getitem__(self, index):
        if self.lista_vazia() or index > self.len:
            raise IndexError
        else:
            count = 0
            for item in self:
                if count == index:
                    return item
                count += 1

    def mostrar_lista(self) -> None:
        if self.lista_vazia():
            print("Lista vazia")
            return None
        for item in self:
            print(item)
        print("\n")

    def lista_vazia(self) -> bool:
        return self.primeiro == None

    def inserir_inicio(self, value: Any) -> None:
        novo = Node(value)
        novo.proximo = self.primeiro
        self.primeiro = novo
        if self.len == 0:
            self.tail = novo
        self.len += 1

    def append(self, value: Any) -> None:
        if self.lista_vazia():
            self.inserir_inicio(value)
        else:
            novo = Node(value)
            self.tail.proximo = novo
            self.tail = novo
            self.len += 1

    def index(self, index: int) -> Node:
        if self.lista_vazia() or index > self.len:
            raise IndexError
        else:
            count = 0
            for item in self:
                if count == index:
                    return item
                count += 1


    def first_ocurrence(self, value: Any) -> None:
        if self.lista_vazia():
            return print('Index fora dos limites da lista')
        else:
            count = 0
            item = self.primeiro
            if item.value == value:
                self.primeiro = self.primeiro.proximo
                self.len -= 1
                return True
            for _ in self:
                if item.proximo is None:
                    return False
                if item.proximo.value == value:
                    item.proximo = item.proximo.proximo
                    if count == self.len-1:
                        self.tail = item
                    break
                item = item.proximo
                count += 1
            self.len -= 1
        return True