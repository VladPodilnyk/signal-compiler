""" Syntax analyser: Lab2 in Compiler development course """

# created by Vlad Podilnyk

from functools import partial

# import lexical analyser and information tables
from scanner import DELIMETERS, KEYWORDS, ID_TABLE, CONST_TABLE
from scanner import scanner
from Node import Node

# reference to the iterator func
next_item = None

COMP_OP = [105, 106, 107, 200, 201, 202]

# maybe
def next_(list_of_tokens):
    """ generator (tmp docstr) """
    index = 0
    lst_length = len(list_of_tokens)
    while index < lst_length:
        yield list_of_tokens[index]
        index += 1

def next_token(gen):
    try:
        return next(gen)
    except StopIteration:
        return [None] * 4

def integer_const(tokens):
    """ func checks int const """
    if tokens[0][0] in range(300, 1000):
        return (Node(tokens[0], "<unsigned-integer>"), tokens[1:])
    else:
        return (Node(None, "ERROR"), None)

def identifier(tokens):
    """ some comment here """
    if tokens[0][0] in range(100, 200):
        return (Node(tokens[0], "<identifier>"), tokens[1:])
    else:
        return (Node(None, "ERROR"), None)

def variable_id(tokens):
    """ var id """
    node = Node(None, "<variable_identifier>")
    child, token_lst = identifier(tokens)
    node.append(child)
    return (node, token_lst)

def procedure_id(tokens):
    """ proc id """
    node = Node(None, "<procedure_identifier>")
    child, token_lst = identifier(tokens)
    node.append(child)
    return (node, token_lst)


def expression(tokens):
    """ describe expression """
    node = Node(None, "<expression>")
    child, token_lst = variable_id(tokens)
    if token_lst is None:
        child, token_lst = integer_const(tokens)
        node.append(child)
        return (node, token_lst)
    else:
        node.append(child)
        return (node, token_lst)

def comparsion_operator(tokens):
    """ comp operarator """
    if tokens[0][0] in COMP_OP:
        return (Node(tokens[0], "<comparsion_operator>"), tokens[1:])
    else:
        return (Node(None, "ERROR"), None)

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
def parser(list_of_tokens):
    gen = next_(list_of_tokens)
    global next_item
    next_item = partial(next_token, gen)




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
