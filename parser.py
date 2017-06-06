""" Syntax analyser: Lab2 in Compiler development course """

# created by Vlad Podilnyk

#TODO write good documentation and comments for functions

# import lexical analyser and information tables
#from scanner import DELIMETERS, KEYWORDS, ID_TABLE, CONST_TABLE
from scanner import scanner
from Node import Node

COMP_OP = [105, 106, 107, 108, 200, 201, 202]

def traversal(tree, order):
    print("{}data:{}\n".format('\t'*order, tree.data), "{}rule:{}\n".format('\t'*order, tree.rule))
    order += 1
    for item in tree.child:
        traversal(item, order)


def integer_const(tokens):
    """ func checks int const """
    if tokens != [] and tokens[0][0] in range(300, 1000):
        return (Node(tokens[0], "<unsigned-integer>"), tokens[1:])
    if tokens == []:
        return (Node(None, "ERROR"), None)
    return (Node(tokens[0], "ERROR"), None)

def identifier(tokens):
    """ some comment here """
    if tokens != [] and tokens[0][0] in range(1000, 5000):
        return (Node(tokens[0], "<identifier>"), tokens[1:])
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

def logical_multiplier(tokens):
    """ keep it up :) sorry, I will add docstring .....soon"""

    lmult = Node(None, "<logical_multiplier>")
    child, tokens_lst = expression(tokens)
    # <expression><comparsion_operator><expression>
    if tokens_lst is not None:
        lmult.append(child)
        child, tokens_lst = comparsion_operator(tokens_lst)
        lmult.append(child)
        if tokens_lst is None:
            return (lmult, None)
        child, tokens_lst = expression(tokens_lst)
        lmult.append(child)
        return (lmult, tokens_lst)

    # <conditional_expression>
    if tokens[0][0] == 205:
        lmult.append(Node(tokens[0], "<DELIMETERS>"))
        child, tokens_lst = conditional_expr(tokens[1:])
        lmult.append(child)
        if tokens_lst is None:
            return (lmult, None)

        if tokens_lst != []:
            if tokens_lst[0][0] == 206:
                lmult.append(Node(tokens_lst[0], "<DELIMETERS>"))
                return (lmult, tokens_lst[1:])
        lmult.append(Node(None, "ERROR"))
        return (lmult, None)

    # NOT <logical_multiplier>
    if tokens[0][0] == 105:
        lmult.append(Node(tokens[0], "<KEYWORDS>"))
        if tokens[1:] == []:
            lmult.append(Node(None, "ERROR"))
            return (lmult, None)

        child, tokens_lst = logical_multiplier(tokens[1:])
        lmult.append(child)
        return (lmult, tokens_lst)

    lmult.append(Node(None, "ERROR"))
    return (lmult, None)


def logical_mult_lst(tokens):
    """ Damn, recursive func """
    log_mult = Node(None, "<logical_multiplier_list>")
    if tokens[0][0] == 104:
        log_mult.append(Node(tokens[0], "<KEYWORDS>"))
        if tokens[1:] == []:
            log_mult.append(Node(None, "ERROR"))
            return (log_mult, None)

        child, tokens_lst = logical_multiplier(tokens[1:])
        log_mult.append(child)
        if tokens_lst is None:
            return (log_mult, None)

        child, tokens_lst = logical_mult_lst(tokens_lst)
        if child is not None:
            log_mult.append(child)
        return (log_mult, tokens_lst)

    return (None, tokens)

def logical(tokens):
    """ logical """
    logic = Node(None, "<logical>")
    if tokens[0][0] == 103:
        logic.append(Node(tokens[0], "<KEYWORDS>"))
        if tokens[1:] == []:
            logic.append(Node(None, "ERROR"))
            return (logic, None)

        child, tokens_lst = logical_summand(tokens[1:])
        logic.append(child)
        if tokens_lst is None:
            return(logic, None)

        log, tokens_lst = logical(tokens_lst)
        if log is not None:
            logic.append(log)
        return (logic, tokens_lst)

    return (None, tokens)


def logical_summand(tokens):
    """ logical summand """
    node = Node(None, "<logical_summand>")
    child, tokens_lst = logical_multiplier(tokens)
    node.append(child)
    if tokens_lst is None:
        return (node, None)
    child, tokens_lst = logical_mult_lst(tokens_lst)
    node.append(child)
    return (node, tokens_lst)

def conditional_expr(tokens):
    """ describe conditional expression """

    cond_expr = Node(None, "<conditional_expression>")
    child, tokens_lst = logical_summand(tokens)
    cond_expr.append(child)
    if tokens_lst is None:
        return (cond_expr, None)

    child, tokens_lst = logical(tokens_lst)
    cond_expr.append(child)
    return (cond_expr, tokens_lst)

def statement(tokens):
    """ your advertisement here """

    node = Node(None, "<statement>")
    child, tokens_lst = variable_id(tokens)
    node.append(child)
    if tokens_lst is None or tokens_lst == []:
        return (node, None)
    # 109 == ':='
    if tokens_lst[0][0] == 109:
        node.append(Node(tokens_lst[0], "<KEYWORDS>"))
        if tokens_lst[1:] == []:
            return (node, None)
        child, tokens_lst = conditional_expr(tokens_lst[1:])
        node.append(child)
        if tokens_lst is None or tokens_lst == []:
            return (node, None)
        # 204 == ';'
        if tokens_lst[0][0] == 204:
            node.append(Node(tokens_lst[0], "<DELIMETERS>"))
            return (node, tokens_lst[1:])
        node.append(Node(None, "ERROR"))
        return (node, None)

    node.append(Node(None, "ERROR"))
    return (node, None)


# statement list
def statement_list(tokens):
    """ bang bang """
    node = Node(None, "<statement_list>")
    child, tokens_lst = statement(tokens)
    node.append(child)
    if tokens_lst is None:
        return (Node(None, "<empty>"), tokens)

    child, tokens_lst = statement_list(tokens_lst)
    node.append(child)
    return (node, tokens_lst)

def declaration(tokens):
    """ declar """
    node = Node(None, "<declaration>")
    child, tokens_lst = variable_id(tokens)
    node.append(child)
    if tokens_lst is None or len(tokens_lst) < 3:
        return (node, None)

    if tokens_lst[0][0] == 203:
        node.append(Node(tokens_lst[0], "<KEYWORDS>"))
        if tokens_lst[1][0] == 110:
            node.append(Node(tokens_lst[1], "<KEYWORDS>"))
            if tokens_lst[2][0] == 204:
                node.append(Node(tokens_lst[2], "<KEYWORDS>"))
                return (node, tokens_lst[3:])

    return (node, None)


# declaration list
def declaration_list(tokens):
    node = Node(None, "<declaration list>")

    if tokens == []:
        node.append(Node(None, "ERROR"))
        return (node, None)

    child, tokens_lst = declaration(tokens)
    node.append(child)
    if tokens_lst is None:
        return (None, tokens)

    child, tokens_lst = declaration_list(tokens_lst)
    node.append(child)
    return (node, tokens_lst)

# variable decrlaration
def var_declaration(tokens):
    """ var decl """
    node = Node(None, "<variable_declarations>")
    if tokens == []:
        node.append(Node(None, "ERROR"))
        return (node, None)

    if tokens[0][0] == 111:
        node.append(Node(tokens[0], "<KEYWORDS>"))
        child, tokens_lst = declaration_list(tokens[1:])
        node.append(child)
        if tokens_lst is None:
            return (node, None)
        return (node, tokens_lst)

    return (None, tokens)

# describe program block
def block(tokens):
    """ smth """
    node = Node(None, "<block>")
    child, tokens_lst = var_declaration(tokens)
    node.append(child)
    if tokens_lst is None:
        return (node, None)

    if tokens_lst != []:
        if tokens_lst[0][0] == 101:
            node.append(Node(tokens_lst[0], "<KEYWORDS>"))
            child, tokens_lst = statement_list(tokens_lst[1:])
            node.append(child)
            if tokens_lst is None:
                node.append(Node(None, "Err"))
                return (node, None)

            if tokens_lst != [] and tokens_lst[0][0] == 102:
                node.append(Node(tokens_lst[0], "<KEYWORDS>"))
                return (node, tokens_lst[1:])

    node.append(Node(tokens_lst[0][1:3], "Error"))
    return (node, None)

def signal_program(tokens):
    node = Node(None, "<program>")
    if tokens != [] and tokens[0][0] == 100:
        node.append(Node(tokens[0], "<KEYWORDS>"))
        child, tokens_lst = procedure_id(tokens[1:])
        node.append(child)
        if tokens_lst is None or tokens_lst == []:
            return (node, None)

        if tokens_lst[0][0] == 204:
            node.append(Node(tokens_lst[0], "<KEYWORDS>"))
            child, tokens_lst = block(tokens_lst[1:])
            node.append(child)
            return (node, tokens_lst)
    node.append(Node(None, "ERROR"))
    return (node, None)

# main fucnction
def parser(list_of_tokens):
    tree, rest = signal_program(list_of_tokens)
    return (tree, rest)



# I made  this part of code for test
if __name__ == "__main__":
    l = scanner("t.txt")
    tree, lexem = parser(l)
    print(lexem)
    print("\n-----------\n")
    traversal(tree, 0)
