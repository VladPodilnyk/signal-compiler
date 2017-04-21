""" Syntax analyser: Lab2 in Compiler development course """

# created by Vlad Podilnyk

# import lexical analyser and information tables
from scanner import DELIMETERS, KEYWORDS, ID_TABLE, CONST_TABLE
from scanner import scanner

# deprecated?
def expr():
    pass

def logical_mult():
    pass

def logical():
    pass

def logical_summand():
    pass

def conditional_expr():
    pass

def statement():
    pass

# statement list
def statement_list():
    pass

def declaration():
    pass

# declaration list
def declaration_list():
    pass

# variable decrlaration
def var_declaration():
    pass

# describe program block
def block():
    pass

def signal_program():
    pass


# main fucnction
def parser():
    pass


# I made  this part of code for test
if __name__ == "__main__":
    l = scanner("t.txt")
    for line in l:
        print("{:>2}:{:>2} {:>5} {}".format(line[1], line[2], line[0], line[3]))

    print(DELIMETERS)
    print('\n____________________________________\n')
    print(KEYWORDS)
    print('\n____________________________________\n')
    print(ID_TABLE)
    print('\n____________________________________\n')
    print(CONST_TABLE)
