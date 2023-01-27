from typing import Any, Union
from types_ import *


def compile_lambda(args: list[Union[Form, Data, Symbol]]) -> callable:
    lambda_params = args[0].args
    lambda_body = args[1:]

    def compiled_lambda(lambda_args):
        global ENV
        # check for number of lambda_args
        if len(lambda_args) != len(lambda_params):
            raise Exception(
                "number of arguments don't match number of parameters")

        # bind the parameters with the values passed in the lambda
        for param, arg in zip(lambda_params, lambda_args):
            ENV[param.name] = ENV.get(param.name, []) + [eval_expr(arg)]

        # execute the body with the new updated env
        res = list(map(eval_expr, lambda_body))[-1]

        # unbind the values from the parameters
        for param in lambda_params:
            ENV[param.name].pop()

        return res
    return compiled_lambda


def eval_expr(expr: Union[Data, Symbol, Form]) -> Any:
    global lambda_count
    global ENV
    if type(expr) == Form:
        # print("expr:",expr)
        fn = eval_expr(expr.args[0])
        # print(fn)
        fn_args = expr.args[1:]
        res = fn(fn_args)
        return res
    elif type(expr) == Data:
        return expr
    elif type(expr) == Symbol:
        if expr.name not in ENV:
            raise Exception(f"{expr} no in current env\n {ENV}")
        return ENV[expr.name][-1]
    else:
        raise Exception("unknown expr type")


ENV = {
    '+': [
        lambda x: Data(sum(map(lambda x: eval_expr(x).val, x)))
    ],
    '-': [
        lambda x: Data(eval_expr(x[0]).val - ENV['+'][-1](x[1:]).val)
    ],
    'lambda': [
        compile_lambda
    ]
}
