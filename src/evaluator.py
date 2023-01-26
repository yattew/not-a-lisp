from typing import Any, Union
from types_ import *
from env import ENV


def compile_lambda(lambda_params: list[Symbol], lambda_body: Form) -> callable:
    def compiled_lambda(lambda_args):
        global ENV
        # check for number of lambda_args
        if len(lambda_args) != len(lambda_params):
            raise Exception(
                "number of arguments don't match number of parameters")

        # bind the parameters with the values passed in the lambda
        for param, val in zip(lambda_params, lambda_args):
            ENV[param.name] = ENV.get(param.name, []) + [val]

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
        # for now lambda is special and seperate from everything else.
        if type(expr.args[0]) == Symbol and expr.args[0] == Symbol("lambda"):
            lambda_params = expr.args[1].args
            lambda_body = expr.args[2:]
            compiled_lambda = compile_lambda(lambda_params, lambda_body)
            return compiled_lambda
        else:
            form_args = list(map(eval_expr, expr.args))
            fn = form_args[0]
            fn_args = form_args[1:]
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
