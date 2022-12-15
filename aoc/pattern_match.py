"""From Raymond Hettinger's 2022 PyCon Italia talk, Structural Pattern Matching in the Real World

https://www.youtube.com/watch?v=ZTvwxXL37XI
"""
import re

class Var:
    pass


class Const:
    pass


class FuncCall:
    def __init__(self, func: callable):
        self.func = func

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return self.func(self.name)


class RegexEqual(str):
    def __eq__(self, pattern):
        return re.fullmatch(pattern, self)