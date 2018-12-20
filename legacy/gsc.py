""" Translator """

import os
import getopt
import sys
from scanner import scanner, LEXER_ERRORS
from parser import parser
from codegen import cgenerator, VAR_TABLE, CONS_TABLE, LABLES_TABLE, ERROR_LOG

def _traverse(tree):
    if tree.rule == "Error":
        print("Syntax Error:{}".format(tree.data[0]))
        return
    for item in tree.child:
        _traverse(item)


def check_lexer_errors(errors):
    if errors == []:
        return
    for err in errors:
        print("Lexical Error:{}:{}".format(err[1], err[2]))
    sys.exit()


def check_syntax_errors(tree, tokens):
    if tokens is not None:
        return
    _traverse(tree)
    sys.exit()


def check_semantic_errors(errors, outputfile):
    if errors == []:
        return
    for err in errors:
        print("Semantic Error:{}:{}".format(err[1], err[2]))
    os.remove(outputfile)
    sys.exit()


def traslator(argv):
    """ BIG BOSS """
    input_file = ""
    output_file = "out.asm"
    if argv == []:
        print("Error: Can't find file to translate.")
        sys.exit()

    try:
        opts, args = getopt.getopt(argv, "i:o:")
    except getopt.GetoptError as err:
        print(err.msg)
        sys.exit()

    if opts == [] and len(argv) == 1:
        input_file = argv[0]
    elif opts == [] and len(argv) > 1:
        print("Error: Too many arguments given.")
        sys.exit()
    else:
        for option, argument in opts:
            if option == "-i":
                input_file = argument
            elif option == "-o":
                output_file = argument


    try:
        tokens_vect = scanner(input_file)
        check_lexer_errors(LEXER_ERRORS)
        tree, tokens_lst = parser(tokens_vect)
        check_syntax_errors(tree, tokens_lst)
        cgenerator(tree, output_file)
        check_semantic_errors(ERROR_LOG, output_file)
    except Exception as err:
        print(err)
        sys.exit()

    print("Success.")


if __name__ == "__main__":
    traslator(sys.argv[1:])
