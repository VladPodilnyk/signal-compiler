""" Lexical analyser: LAB1 in Compiler development course """

# created by Vlad Podilnyk
import sys

# description of standart tables (keywords, delimeters, allowed symbols)

KEYWORDS = {'PROGRAM': 100,
            'BEGIN': 101,
            'END': 102,
            'OR': 103,
            'AND': 104,
            'NOT': 104,
            '<=': 105,
            '>=': 106,
            '<>': 106}

DELIMETERS = {'<': 200,
              '>': 201,
              '=': 202,
              ':': 203,
              ';': 204,
              '(': 205,
              ')': 206}

ID_TABLE = {}

# functions for initializing basic tables

def init_attr_vector(attr_vect):
    """ The function inits an attribute vector """

    # 0 - space, eof, eol, etc
    # 1 - 0..9
    # 2 - a-z or A-Z
    # 3 - =, :, ;, ')' - one-character delimeter
    # 4 - <, > - first symbols of complex-delimeters (>=, <>, <=)
    # 5 - '(' - commentary  --> (*.....*)
    # 6 - other

    attr_vect = [6] * 128
    attr_vect[40] = 5
    attr_vect[41] = 3
    attr_vect[58] = 3
    attr_vect[59] = 3
    attr_vect[60] = 4
    attr_vect[61] = 3
    attr_vect[62] = 4
    for index in range(128):
        if index in range(0, 33):
            attr_vect[index] = 0
        elif index in range(48, 58):
            attr_vect[index] = 1
        elif index in range(65, 91) or index in range(97, 123):
            attr_vect[index] = 2

def add_to_table(value):
    """ The function adds token to an ID_TABLE and returns an appropriate code,\
     if token has already in ID_TABLE then just returns a code"""

    if value in KEYWORDS.keys():
        return KEYWORDS[value]

    elif value in DELIMETERS.keys():
        return DELIMETERS[value]

    elif value in ID_TABLE.keys():
        return ID_TABLE[value]

    else:
        ID_TABLE[value] = len(ID_TABLE) + 1000
        return ID_TABLE[value]


def scanner(file_name):
    """ The function reads terms from a file, checks them and replaces with special code """

    try:
        source = open(file_name, 'r')
    except FileNotFoundError as err:
        print("[ERROR]::{}".format(err.strerror))
        return

    # ruesult_lst consists encoded information about all tokens from input file
    result_lst = []

    # information about token; indexes: 0->code, 1->row, 2->column, 3->real value
    token = []

    word_buffer = ''

    while True:
        symbol = source.read(1)
        if not symbol:
            raise Exception("[ERROR]::Empty file")



    source.close()

if __name__ == '__main__':
    print("Have a nice day!!!")
    scanner("k.txt")












