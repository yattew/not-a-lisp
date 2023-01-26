from typing import Any


class Symbol:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"[sym {self.name}]"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name


class Data:
    def __init__(self, val: Any) -> None:
        self.val = val

    def __repr__(self) -> str:
        return f"{self.val}"

    def __str__(self) -> str:
        return self.__repr__()


class Form:
    def __init__(self, args: list) -> None:
        self.args = args

    def __repr__(self) -> str:
        res = "("
        for i in self.args:
            res += str(i)+' '
        res += ')'
        return res

    def __str__(self) -> str:
        return self.__repr__()
