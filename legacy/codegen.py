"""Code generator: Lab3 in Compiler development course """

from scanner import scanner
from parser import parser

OP_STACK = []
INS_STACK = []
VAR_TABLE = {}
CONS_TABLE = {}
LABLES_TABLE = []
ERROR_LOG = []
PR_NAME = None
INSTR = ["OR", "AND", "NOT", "[", "]"]
FILE = None
JUMPS = {
    "<>": "jne",
    "<" : "jl",
    ">" : "jg",
    ">=": "jge",
    "<=": "jle",
    "=" : "je",
}

REG = {
    1: "eax",
    2: "ebx",
    3: "ecx",
    4: "edx",
}


PRIORITY = {
    "OR" : 0,
    "AND": 1,
    "NOT": 2
}

CURR_REG = 1
LABLE_NUM = 1

def is_valid(operand):
    if operand != PR_NAME and operand in VAR_TABLE.keys() and VAR_TABLE[operand][-1] == 1:
        return True
    return False

def generate_text():
    global FILE
    FILE.write("\nsegment .text\n\tglobal _start\n_start:\n")
    LABLES_TABLE.append("_start")

def generate_bss(subtree):
    global FILE
    variable = subtree.child[0].data
    if variable[-1] in VAR_TABLE.keys() or variable[-1] == PR_NAME:
        ERROR_LOG.append(variable)
    else:
        VAR_TABLE[variable[-1]] = [variable, 0]
        FILE.write("\t{} resd 1\n".format(variable[-1]))

def generate_cond(first_operand, condition, second_operand):
    global CURR_REG
    global LABLE_NUM
    global FILE
    register = first_operand.child[0]
    operand = second_operand.child[0]
    if register.rule == "<unsigned-integer>" and register.data[-1] not in CONS_TABLE.keys():
        CONS_TABLE[register.data[-1]] = register.data
    elif register.rule == "<variable_identifier>":
        if not is_valid(register.child[0].data[-1]):
            ERROR_LOG.append(register.child[0].data)
        register = register.child[0]

    if operand.rule == "<unsigned-integer>" and operand.data[-1] not in CONS_TABLE.keys():
        CONS_TABLE[operand.data[-1]] = operand.data
    elif operand.rule == "<variable_identifier>":
        if not is_valid(operand.child[0].data[-1]):
            ERROR_LOG.append(operand.child[0].data)
        operand = operand.child[0]

    FILE.write("\tmov {}, {}\n".format(REG[CURR_REG], register.data[-1]))
    FILE.write("\tcmp {}, {}\n\t{} label{}\n".format(REG[CURR_REG], operand.data[-1],
                                                     JUMPS[condition.data[-1]], LABLE_NUM))

    FILE.write("\t\tmov {}, 0\n\t\tjmp label{}\n".format(REG[CURR_REG], LABLE_NUM + 1))
    FILE.write("\tlabel{}:\n\t\tmov {}, 1\n".format(LABLE_NUM, REG[CURR_REG]))
    FILE.write("\tlabel{}:\n\n".format(LABLE_NUM + 1))
    OP_STACK.append(REG[CURR_REG])
    LABLE_NUM += 2
    CURR_REG += 1


def clean_up_stack(variable):
    global CURR_REG
    global FILE
    #print(OP_STACK)
    #print(INS_STACK)
    while INS_STACK != []:
        if INS_STACK[-1] == "NOT":
            FILE.write("\t{} {}\n".format(INS_STACK.pop(), OP_STACK[-1]))
        else:
            operand = OP_STACK.pop()
            result = OP_STACK[-1]
            FILE.write("\t{} {}, {}\n".format(INS_STACK.pop(), result, operand))

    FILE.write("\tmov [{}], {}\n".format(variable.data[-1], OP_STACK[-1]))
    CURR_REG = 1
    OP_STACK.pop()
    if variable.data[-1] in VAR_TABLE.keys():
        VAR_TABLE[variable.data[-1]][-1] = 1
    else:
        ERROR_LOG.append(variable.data)


def switch(subtree):
    """ generates code which is depends on condition """
    global PR_NAME
    global CURR_REG
    global FILE
    if subtree.rule == "<procedure_identifier>":
        PR_NAME = subtree.child[0].data[-1]
        return True
    elif subtree.rule == "<variable_declarations>":
        FILE.write("segment .bss\n")
        return False
    elif subtree.rule == "<declaration>":
        generate_bss(subtree.child[0])
        return True
    elif subtree.rule == "<KEYWORDS>" and subtree.data[0] == 101:
        generate_text()
        return False
    elif subtree.rule == "<KEYWORDS>" and subtree.data[0] == 102:
        FILE.write("\tmov eax, 1\n\tint 0x80\n")
        return False
    elif subtree.rule == "<empty>":
        FILE.write("\n\tnop\n\n")
        return False

    elif subtree.rule == "<statement>":
        code_generator(subtree.child[2])
        clean_up_stack(subtree.child[0].child[0])
        return True

    elif subtree.rule == "<logical_multiplier>" and subtree.child[0].rule == "<expression>":
        generate_cond(subtree.child[0], subtree.child[1], subtree.child[2])
        return True

    elif (subtree.rule == "<KEYWORDS>" or subtree.rule == "<DELIMETERS>")\
    and subtree.data[-1] in INSTR:
        if INS_STACK == [] or subtree.data[-1] == "[" or INS_STACK[-1] == "[":
            INS_STACK.append(subtree.data[-1])

        elif subtree.data[-1] == "]":
            while INS_STACK[-1] != "[":
                if INS_STACK[-1] == "NOT":
                    while INS_STACK[-1] == "NOT":
                        FILE.write("\t{} {}\n".format(INS_STACK.pop(), OP_STACK[-1]))
                else:
                    operand = OP_STACK.pop()
                    result = OP_STACK[-1]
                    FILE.write("\t{} {}, {}\n".format(INS_STACK.pop(), result, operand))
                    CURR_REG -= 1
            INS_STACK.pop()

        elif PRIORITY[subtree.data[-1]] > PRIORITY[INS_STACK[-1]] or subtree.data[-1] == "NOT":
            INS_STACK.append(subtree.data[-1])

        else:
            if INS_STACK[-1] == "NOT":
                while INS_STACK[-1] == "NOT":
                    FILE.write("\t{} {}\n".format(INS_STACK.pop(), OP_STACK[-1]))
                if PRIORITY[subtree.data[-1]] <= PRIORITY[INS_STACK[-1]]:
                    operand = OP_STACK.pop()
                    result = OP_STACK[-1]
                    FILE.write("\t{} {}, {}\n".format(INS_STACK.pop(), result, operand))
                    CURR_REG -= 1
            else:
                operand = OP_STACK.pop()
                result = OP_STACK[-1]
                FILE.write("\t{} {}, {}\n".format(INS_STACK.pop(), result, operand))
                CURR_REG -= 1
            INS_STACK.append(subtree.data[-1])
    else:
        return False


def code_generator(tree):
    """ Generate assembly code with black jack and sluts """
    #print(tree.rule)
    if switch(tree):
        return
    for item in tree.child:
        code_generator(item)

def cgenerator(tree, filename):
    """ main function """
    global FILE
    with open(filename, "w") as FILE:
        code_generator(tree)



if __name__ == "__main__":
    lexems = scanner("t.txt")
    tree, tokens = parser(lexems)
    cgenerator(tree, "out.asm")
    print(ERROR_LOG)

