# Dynamic Hash Table - Linear Hash
# Autor: Jonathan Willian dos Santos
# Ultima Atualizacao: 08/04/2023

# Referenciais:
# 1 - https://www.csd.uoc.gr/~hy460/pdf/Dynamic%20Hash%20Tables.pdf
# 2 - https://citeseerx.ist.psu.edu/doc/10.1.1.14.5908
# 3 - https://planetmath.org/goodhashtableprimes

# Explicarei como a impletancao funciona, mas para melhor entendimento recomendo
# acessar a referencia 1
#
# Basicamente temos uma estrutura com duas camadas chamadas DIRECTORY e SEGMENT
# O directory eh um array de segments e os segments sao arrays de listas linkadas,
# que chamarei de bucket
#                                              
# D         
# I       _      ...    
# R      |_|      |
# E      |_|     [1]
# C      |_|      |
# T  [2] |_|     [0] CABEÇA DO BUCKET
# O  [1] |_|      |  _  _  _
# R  [0] |_| --> |_||_||_||_|
# Y                SEGMENTS
#
# Para manter uma distribuicao nivelada de colisao tentaremos manter uma media de 
# 5 NODOS por BUCKET
# Esse esquema esta melhor explicado na funcao .EXPAND_TABLE()
#
# Mas basicamente temos um atributo que guarda o proximo bucket a ser SPLITADO,
# esse bucket tera seus itens dividos com um novo BUCKET recem alocado quando atingirmos
# um limite dado por UPPER_BOUND. 
# Fazemos isso para cada BUCKET do SEGMENTO e quando chegarmos no final do SEGMENTO
# um novo sera alocado e comecaremos a splitar do inicio.



from typing import Any

# Numpy foi usado apenas para as estatisticas referentes a colisoes 
import numpy as np

MINIMUN_SIZE = 256
DIRECTORY_MAXIMUM_LENGTH = 256
SEGMENTS_MAXIMUM_LENGTH = 256
PRIME = 104883
UPPER_BOUND = 5
LOWER_BOUND = 0

class Node:
    """
    A menor estrutura dentro da nossa Hash Table, guardando o valor e a key.
    Nao ha uma estrutura separada que agrupe os nodos, apenas o atributo que 
    aponta para o proximo
    """
    def __init__(self, key, value: Any) -> None:
        self.value: Any = value
        self.key: str = key
        self.next: Node | None = None

class Segment:
    """
    Esta classe funciona como uma lista de listas linkadas. Sua principal
    funcao eh guardar o ponteiro para o primeiro nodo de cada bucket

    Se eh uma lista de lista linkadas, pq os elementos sao nodos?
    Preferi nao criar uma estrutura separada para as listas linkadas, pois assim
    tenho mais flexibilidade para mover os nodos dentro dos segmentos e para outros
    segmento. 

    As funcoes colisions e count_nodes existem por pura funcao estatistica, 
    afim de identificar a performance da Hash Table em relacao a colisoes
    """
    def __init__(self) -> None:
        self.bucket_list: list[Node | None] = [None] * SEGMENTS_MAXIMUM_LENGTH

    def __getitem__(self, i: int) -> None | Node:
        return self.bucket_list[i]

    def __setitem__(self, i: int, value: Any) -> None:
        self.bucket_list[i] = value

    def colisions(self) -> np.ndarray:
        """
        Conta a quantidade de nodos em cada bucket da lista de buckets.
        Essa funcao nos diz quanto eh a quantidade total de colisoes
        """
        colision_distribuition = np.array(
            list(map(self.count_nodes, self.bucket_list)))
        return colision_distribuition

    @staticmethod
    def count_nodes(node: 'Node') -> int:
        count = 0
        while node is not None:
            count += 1
            node = node.next
        return count


class HashTable:
    """
    Hash Table Dinamica utilizando Linear Hash
    
    Aloca um novo segmento quando a media de itens nos buckets for maior que
    upper bound

    as funcoes principais sao FIND, INSERT e REMOVE

    A funcao hash utiliza um numero PRIMO longo, estando implementada em .ADRESS()

    Voce pode utilizar a estrutura passando chave, valor para a funcao de INSERT 
    e apenas a chave para FIND e REMOVE

    """

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

        self.current_seg_i: int = 0
        self.current_bkt_i: int = 0
        self.current_nodo: Node | None = None 

    def __len__(self) -> int:
        return self.length
    
    def __iter__(self):
        self.current_seg_i = 0
        self.current_bkt_i = 0
        seg = self.directory[self.current_seg_i]
        self.current_nodo = seg[self.current_bkt_i]
        return self

    def __next__(self):
        """
        Itera ate achar um NODO que nao seja VAZIO. A condicao principal de parada
        é encontrar um diretório vazio.

        Como os valores estao distribuidos de forma aleatorio dentro do segmento eh
        necessario percorrer ele inteiramente. 

        Quando encontra um NODO que nao eh NONE retorna e seta as variaveis de control
        de iteracao para o proximo.
        """
        seg = self.directory[self.current_seg_i]
        
        if seg is None or self.current_seg_i > DIRECTORY_MAXIMUM_LENGTH:
            raise StopIteration
        else:
            no_atual = self.current_nodo
            
            while no_atual is None:
                self.current_bkt_i += 1
                if self.current_bkt_i > SEGMENTS_MAXIMUM_LENGTH - 1:
                    self.current_bkt_i = 0
                    self.current_seg_i += 1
                
                    if self.current_seg_i > DIRECTORY_MAXIMUM_LENGTH - 1:
                        raise StopIteration

                    seg = self.directory[self.current_seg_i]

                    if seg is None:
                        raise StopIteration

                no_atual = seg[self.current_bkt_i]

            self.current_nodo = no_atual.next
            
        return (no_atual.key, no_atual.value)
    
    def show(self):
        count = 0
        print('{', end='')
        for key, value in self:
            print(f'{key}: {value}', end='')
            count += 1
            if count != self.length:
                print(',', end=' ')
        print('}')


    @staticmethod
    def str2int(string: str) -> int:
        """
        Funcao auxiliar para converter uma string para inteiro
        """
        string = string.encode('ascii')
        return int.from_bytes(string, byteorder='big')

    def address(self, key: str) -> int:
        """
        Calcula o endereco que sera ou esta alocada a key.
        Se o endereco pertencer a um bucket ja splitado, recalcula o endereco 
        """
        key = self.str2int(key)
        h: int = key % PRIME
        addr: int = h % self.maxp
        if addr < self.next_bucket:
            addr = h % (self.maxp * 2)
        return addr

    def find_head(self, key: str) -> Node:
        """
        Acha o primeiro elemento de um bucket 

        Primeiro acha o segmento a qual pertence esse endereco e 
        depois procura o index desse endereco dentro do segmento.

        retorna o nodo que eh a cabeca do bucket
        """
        addr: int = self.address(key)
        current_segment: Segment = self.directory[addr //
                                                  DIRECTORY_MAXIMUM_LENGTH]
        segment_i: int = addr % SEGMENTS_MAXIMUM_LENGTH
        return current_segment[segment_i]

    def find(self, key: str) -> Any:
        """
        Acha a cabeca do segmento no qual essa key esta alocada e 
        depois itera sobre os elementos do bucket ate achar o elemento
        """
        current_node: Node = self.find_head(key)
        while current_node != None:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next

    def get_keys(self) -> list[str]:
        """
        Funcao que retorna as keys presentes no dicionario. 

        Essa funcao eh auxiliar e nao pertenceria a implementacao se nao fosse 
        por questoes de estudo. Adicionar um novo elemento na lista de keys eh
        relativamente barato -> O(1), porem remover nao eh -> O(n), o que afetaria bastante
        a performance do .remove() 

        Por isso, em remove, nao retiro a key da lista. Uso essa funcao mais para debug e para
        brincar um pouco com a implementacao e entender melhor como ela funciona.
        """
        return self.keys

    def insert(self, key: str, value: Any) -> None:
        """
        Primeiro checa se a media de itens por chain nao excedeu o UPPER_BOUND. Se sim, expande.

        Se o index do segmento ja esta ocupado, ou seja, se houve colisao, itera no bucket ate
        achar um espaco livre.
        """
        if self.length / self.maxp > self.upper_bound:
            self.expand_table()

        new_node: Node = Node(key, value)

        addr = self.address(key)

        # Procura pelo segmento e pelo index do segmento que esse endereco esta 
        segment: Segment = self.directory[addr //
                                                  SEGMENTS_MAXIMUM_LENGTH]
        segment_i: int = addr % DIRECTORY_MAXIMUM_LENGTH
        current_node: Node | None = segment[segment_i]

        if current_node == None:
            segment[segment_i] = new_node
        else:
            while current_node.next != None:
                current_node = current_node.next
            current_node.next = new_node

        # self.keys.append(key) # Remover aqui se for terminar a implementacao
        self.length += 1

    def expand_table(self) -> None:
        """
        Faz a expancao dinamica da hash table. 
        
        Primeiro checa se a hash table nao excedeu seu limite maximo. 

        Nossa estrutura splita um bucket por vez, mantendo um contador do proximo
        bucket a ser splitado no atributo NEXT_BUCKET.

        Mantemos tambem o limite que esse NEXT_BUCKET pode chegar em MAXP

        Calculamos um novo endereco baseado no bucket que estamos splitando, se for 
        necessario alocamos um novo SEGMENTO no DIRECTORY. Cada NODE desse BUCKET 
        sofrera um  "rehash", ou seja, seu endereco sera calculado novamente. Se o endereco 
        recalculado for igual ao novo endereco entao ele sera alocado no novo bucket. 
        
        Ao chegarmos ao final do primeiro segmento, ou seja, se fizemos o split em 
        todos os buckets, entao dizemos que a table teve seu tamanho dobrado e 
        resetamos o valor de NEXT_BUCKET, comecando os splits do inicio e o MAXP 
        agora sera calculado com base no novo tamanho da table, que foi dobrada
        (atributo DOUBLED).

        Dessa forma mantemos uma distribuicao mais nivelada das colisoes.

        Ha um exemplo visual desse esquema em: referencia 1 - FIGURE 1.
        """
        if self.maxp + self.next_bucket < DIRECTORY_MAXIMUM_LENGTH * SEGMENTS_MAXIMUM_LENGTH:

            # Novo endereco calculado a partir do bucket que sofrera o split
            new_addr: int = self.maxp + self.next_bucket

            # Calculamos o endreco do novo bucket. Se for necessario, adicionamos
            # um novo SEGMENT no diretorio para alocar os NODES
            directory_i = new_addr // SEGMENTS_MAXIMUM_LENGTH
            if new_addr % SEGMENTS_MAXIMUM_LENGTH == 0:
                self.new_segment(directory_i)

            new_segment: Segment = self.directory[directory_i]
            new_segment_i: int = new_addr % SEGMENTS_MAXIMUM_LENGTH

            old_segment: Segment = self.directory[self.next_bucket //
                                                  SEGMENTS_MAXIMUM_LENGTH]
            old_segment_i: int = self.next_bucket % SEGMENTS_MAXIMUM_LENGTH

            # Se ja splitamos todos os buckets do segmento entao quer dizer
            # que dobramos a table de tamanho. Sera necessario alocar mais um
            # SEGMENT quando passarmos por essa funcao novamente.
            # Tambem setamos NEXT_BUCKET para 0 pois sera feito o split do comeco
            self.next_bucket += 1
            if self.next_bucket == self.maxp:
                self.doubled += 1
                self.maxp = MINIMUN_SIZE * 2**self.doubled
                self.next_bucket = 0

            # Faz a alocao dos NODES no novo BUCKET
            current_node: Node = old_segment[old_segment_i] # Nodo que esta sofrendo o REHASH
            new_segment[new_segment_i]: Node | None = None  # Novo segmento que esta  
            previous: Node | None = None                    # current_node anterior 
            last_of_new: Node | None = None                 # TAIL do novo segmento

            while current_node != None:

                if self.address(current_node.key) == new_addr:

                    if last_of_new == None:
                        new_segment[new_segment_i] = current_node
                    else:
                        last_of_new.next = current_node

                    if previous == None:
                        old_segment[old_segment_i] = current_node.next
                    else:
                        previous.next = current_node.next

                    last_of_new = current_node
                    current_node = current_node.next
                    last_of_new.next = None
                else:
                    previous = current_node
                    current_node = current_node.next

    def new_segment(self, i: int) -> None:
        self.directory[i] = Segment()

    def remove(self, key: str) -> None:
        """
        .REMOVE() foi implementado parcialmente. Como eh uma hash table dinamica, 
        o correto seria dimuir o tamanho dela ao bater o valor do LOWER_BOUND. 

        Mas nessa atividade optei por melhorar a documentacao e os testes ao 
        inves de implementar a funcao SHRINK_TABLE.
        Nao acredito que seja tao trivial a implementacao dessa funcao, conside_
        rando que a EXPAND_TABLE(), apesar de simples, me custou algumas horas.  
        """
        current_node: Node = self.find_head(key)

        if current_node is None:
            return

        # Se o primeiro nodo do segmento[i] for o procurado
        if current_node.key == key:
            addr: int = self.address(key)
            current_segment: Segment = self.directory[addr //
                                                      SEGMENTS_MAXIMUM_LENGTH]
            segment_i: int = addr % DIRECTORY_MAXIMUM_LENGTH
            current_segment[segment_i] = current_node.next
        # senao procura ele nos proximos nodos
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

    def stats(self) -> dict:
        """
        Auxiliar para obter as estatisticas de colisoes

        collisions_list eh um ndarray de inteiros. Os elementos desse array
        sao os tamanhos das listas linkadas

        Como os nodos nao estao organizados dentro de uma estrutura eh necessario
        iterar sobre cada um deles para calcular o tamanho. Nao eh nada eficiente, mas
        como estou utilizando apenas para as estatisticas achei que seria o suficiente.
        """
        i = 0
        current_dir: Segment = self.directory[i]
        collisions_list: np.ndarray[int] = np.array([])  
        while current_dir is not None:
            collisions_list = np.append(
                collisions_list, current_dir.colisions())
            i += 1
            current_dir = self.directory[i]

        collisions_list = np.sort(collisions_list)
        stats: dict = {}
        stats['median'] = np.median(collisions_list)
        stats['average'] = np.mean(collisions_list)
        stats['max'] = np.max(collisions_list)
        stats['min'] = np.min(collisions_list)

        return stats, collisions_list


if __name__ == '__main__':
    from TesteFuncUtils import *
    a = HashTable()
    
    for n in range(100):
        a.insert(make_rand_str(LENGTH_RAND_STR), n)
    # a.insert(make_rand_str(LENGTH_RAND_STR), 1)
    
    a.show()
    
        
