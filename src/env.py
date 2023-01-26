from typing import Any, Union
from types_ import *


def add(x: list[Union[Data, Symbol]]) -> Data:
    global ENV
    res = 0
    for i in x:
        if type(i) == Data:
            res += i.val
        elif type(i) == Symbol:
            res += ENV[i.name][-1].val
        else:
            raise Exception(f"type of {i} is unknown")
    return Data(res)


def sub(x: list[Union[Data, Symbol]]) -> Data:
    global ENV
    res = x[0]
    for i in x[1:]:
        if type(i) == Data:
            res -= i.val
        elif type(i) == Symbol:
            res -= ENV[i.name][-1].val
        else:
            raise Exception(f"type of {i} is unknown")
    return Data(res)


ENV = {
    '+': [
        add
    ],
    '-': [
        sub
    ],
}
