""" Lexical analyser: LAB1 in Compiler development course """

# created by Vlad Podilnyk

# description of standart tables (keywords, delimeters, allowed symbols)

KEYWORDS = {'PROGRAM': 100,
            'BEGIN': 101,
            'END': 102,
            'OR': 103,
            'AND': 104,
            'NOT': 104,
            '<=': 105,
            '>=': 106,
            '<>': 106,
            ':=': 107,
            'INTEGER': 108}

DELIMETERS = {'<': 200,
              '>': 201,
              '=': 202,
              ':': 203,
              ';': 204,}

ID_TABLE = {}

CONST_TABLE = {}

# functions for initializing basic tables

def init_attr_vector():
    """ The function inits an attribute vector """

    #------------attributes------------
    # 0 - space, eof, eol, etc
    # 1 - 0..9
    # 2 - a-z or A-Z
    # 3 - =, :, ;, ')' - one-character delimeter
    # 4 - <, > - first symbols of complex-delimeters (>=, <>, <=)
    # 5 - '(' - commentary  --> (*.....*)
    # 6 - other

    attr_vect = [6] * 128
    attr_vect[40] = 5
    attr_vect[41] = 6
    attr_vect[58] = 4
    attr_vect[59] = 3
    attr_vect[60] = 4
    attr_vect[61] = 3
    attr_vect[62] = 4
    for indx in range(128):
        if indx in range(0, 33):
            attr_vect[indx] = 0
        elif indx in range(48, 58):
            attr_vect[indx] = 1
        elif indx in range(65, 91) or indx in range(97, 123):
            attr_vect[indx] = 2

    return attr_vect

def add_to_id_table(value):
    """ The function adds token to an ID_TABLE and returns an appropriate code\
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

def add_to_cons(value):
    """ The function adds integer constants to a CONST_TABLE and returns an appropriate code\
    if constant has already in CONST_TABLE then just returns a code """

    if value in CONST_TABLE.keys():
        return CONST_TABLE[value]

    else:
        CONST_TABLE[value] = len(CONST_TABLE) + 300
        return CONST_TABLE[value]


def index(value):
    """ The function checks whether a symbol is valid or not """
    if ord(value) > 127:
        return 127
    return ord(value)




def scanner(file_name):
    """ The function reads terms from a file, checks them and replaces with special code """

    try:
        source = open(file_name, 'r')
    except FileNotFoundError as err:
        print("[ERROR]::{}".format(err.strerror))
        return

    # ruesult_lst consists encoded information about all tokens from input file
    result_lst = []

    # attribute vector initialization
    attr_vector = init_attr_vector()

    symbol = source.read(1)
    if not symbol:
        raise Exception("[ERROR]::Empty file")

    row = 1
    column = 0

    while symbol:
        word_buffer = ''
        # a finite state machine realization
        # the finite state machine has 7 states that correspond to 7 types of attributes

        # 0 - space, eof, eol, etc
        if attr_vector[index(symbol)] == 0:
            while symbol and attr_vector[ord(symbol)] == 0:
                if ord(symbol) == 10:
                    row += 1
                    column = 0
                else:
                    column += 1
                symbol = source.read(1)

        # 1 - integer constants
        elif attr_vector[index(symbol)] == 1:
            column += 1
            while symbol and attr_vector[ord(symbol)] == 1:
                word_buffer += symbol
                symbol = source.read(1)
            result_lst.append([add_to_cons(word_buffer), row, column, word_buffer])
            column += len(word_buffer) - 1

        # 2 - identifier
        elif attr_vector[index(symbol)] == 2:
            column += 1
            while symbol and (attr_vector[ord(symbol)] == 2 or attr_vector[ord(symbol)] == 1):
                word_buffer += symbol.upper()
                symbol = source.read(1)
            result_lst.append([add_to_id_table(word_buffer), row, column, word_buffer])
            column += len(word_buffer) - 1

        # 3 - delimeters(=, ;, :)
        elif attr_vector[index(symbol)] == 3:
            column += 1
            result_lst.append([DELIMETERS[symbol], row, column, symbol])
            symbol = source.read(1)

        # 4 - complex delimeters (>=, <=, <>)
        elif attr_vector[index(symbol)] == 4:
            word_buffer += symbol
            symbol = source.read(1)
            word_buffer += symbol
            if word_buffer in KEYWORDS.keys():
                column += 2
                result_lst.append([KEYWORDS[word_buffer], row, column, word_buffer])
                symbol = source.read(1)
            else:
                column += 1
                result_lst.append([DELIMETERS[word_buffer[0]], row, column, word_buffer[0]])

        # 5 - comments
        elif attr_vector[index(symbol)] == 5:
            flag = False
            symbol = source.read(1)
            if symbol == '*':
                column += 2
                while symbol:
                    symbol = source.read(1)
                    if symbol == '\n':
                        row += 1
                        column = 0
                    elif symbol == '*':
                        symbol = source.read(1)
                        if symbol == ')':
                            column += 2
                            break
                    column += 1
                if flag:
                    raise Exception("[ERROR]::Expected '*)' but end of file found")
                symbol = source.read(1)
            else:
                column += 1
                result_lst.append(['ERROR', row, column, '('])

        # 6 - errors
        elif attr_vector[ord(symbol)] == 6:
            column += 1
            result_lst.append(['ERROR', row, column, symbol])
            symbol = source.read(1)

    source.close()
    return result_lst


# under tests
if __name__ == '__main__':
    print("Have a nice day!!!")
    l = scanner("t.txt")
    for line in l:
        print("{:>2}:{:>2} {:>5} {}".format(line[1], line[2], line[0], line[3]))
