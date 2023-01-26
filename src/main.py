from typing import Any, Union

from types_ import *
from parser_ import *
from evaluator import *


def main() -> None:
    from sys import argv
    file_name = argv[1]
    text = ""
    with open(file_name, "r") as f:
        text = f.read()
    expr = parse_expr(text)
    res = eval_expr(expr)
    print(res)


if __name__ == "__main__":
    main()
