# Desenvolvimento dessas funcoes foram feitas de foram bem simples  
# e rasteira. A intecao era apenas usar o layout nos teste
# 
# .-----------------------------------.
# |          TESTE_NAME                |
# |----------------------------------- |
# |  FUNC  | EXCS |   SIZE |   TIME    |
# |--------|------|--------|-----------|
# | insert |      |        |           |
# | remove |      |        |           |
# | find   |      |        |           |
# | Hash   |      |        |           |
# *------------------------------------*
from configTestes import * 

def str_horizontal(chars, amount):
    string = chars[0]
    string += chars[1]*amount
    string += chars[0]
    return string 

def str_vertical(char, amount, width):
    string = ''
    string += '\n'
    for _ in range(amount):
        string += (char + ' '*width + char + '\n')
    return string

def str_test_name(name, width, char):
    string = '\n'
    string += char
    string += name.center(width)
    string += char
    string += '\n'
    string += str_horizontal('|-', width)
    return string

def str_layout(values, width=WIDTH, heigth=HEIGTH):
    string = ''
    string += str_horizontal('.-', width)
    string += str_test_name(NAME, width, '|')
    string += '\n'
    string += str_columns(COLUMN_NAMES, width, '|')
    string += '\n'
    string += str_columns(['-'*(width//4)] * 4, width, '|')

    for item in values:
        string += '\n'
        string += str_columns(item, width, '|')

    string += str_vertical('|', heigth, width)
    string += str_horizontal('*-', width)
    return string

def str_columns(values, width, char):
    string = ''

    for n in range(4):
        string += char
        string += values[n].center(width//4)
    
    string += char

    return string


if __name__ == '__main__':
    print(str_layout([['insert', '10', '55', '10'], ['insert', '10', '55', '10'], ['insert', '10', '55', '10'], ['insert', '10', '55', '10']],WIDTH, HEIGTH))