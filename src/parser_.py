from typing import Any, Union
from types_ import *


def empty_char(x):
    return x == ' ' or x == '\n' or x == '\t'


def create_form(string: str) -> Form:
    form_list = []  # intermediatary var, will contain the argument list for final 'Form'
    temp = ""
    i = 0
    while i < len(string):
        # print("form create for i:", i)
        if string[i] == '(':
            # print("here")
            curr_lbracks = 0
            temp_str = ""
            j = i
            while j < len(string):
                if string[j] == '(':
                    curr_lbracks += 1
                elif string[j] == ')':
                    curr_lbracks -= 1
                temp_str += string[j]
                if curr_lbracks == 0:
                    break
                j += 1
            i = j+1  # start the next iteration after the closing paren
            # parse whatever is inside temp_str and get the form
            this_form: Form = parse_expr(temp_str)
            form_list.append(this_form)  # add this form to form_list
        elif empty_char(string[i]):  # empty space to be ignored
            i += 1
        else:  # could be a number or a string
            j = i
            data_str = ""
            # as soon as there is a space it means the str/num has ended
            while j < len(string) and not empty_char(string[j]):
                data_str += string[j]
                j += 1
            # will take care of number and str and return appropriate instance of Data class
            data: Data = parse_expr(data_str)
            # append this as another argument to the form_list
            form_list.append(data)
            i = j+1  # start next iteration from the next char after str/num is parsed

    final_form = Form(form_list)
    return final_form


def parse_expr(string: str) -> Union[Data, Symbol, Form]:
    string = string.strip(" \n")
    ch = string[0]
    if ch.isdigit():
        return Data(int(string))
    elif ch == '"':
        return Data(string[1:-1])
    elif ch == "(":
        form = create_form(string[1:-1])
        return form
    else:
        return Symbol(string)


def test_parser() -> None:
    tests = [
        "1",
        '"hello world"',
        "(+ 1 2)",
        "(+ (- 1 2) 10)",
        "((lambda () (+ 1 10)))",
        "((lambda (x) (+ 1 x)) 10)"
    ]
    for i, v in enumerate(tests):
        print(f"test[{i}]   {v}: \n->\t{parse_expr(v)}\n")
