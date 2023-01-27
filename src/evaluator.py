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
    global ENV
    match expr.__class__.__name__:
        case Form.__name__:
            fn = eval_expr(expr.args[0])
            fn_args = expr.args[1:]
            return fn(fn_args)
        case Data.__name__:
            return expr
        case Symbol.__name__:
            if expr.name not in ENV:
                raise Exception(f"{expr} no in current env\n {ENV}")
            return ENV[expr.name][-1]
        case _:
            raise Exception(f"unknown expr type \n{[type(expr)]} {expr}")

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
