""" Tree node """

class Node:
    """ Tree node implementation """

    def __init__(self, data, rule, parent=None):
        self.__data = data
        self.__child = []
        self.__parent = parent
        self.__rule = rule

    @property
    def data(self):
        return self.__data

    @property
    def rule(self):
        return self.__rule

    @property
    def child(self):
        return self.__child

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, parent):
        self.__parent = parent

    @data.setter
    def data(self, data):
        self.__data = data

    @rule.setter
    def rule(self, rule):
        self.__rule = rule

    def append(self, node):
        self.child.append(node)
