import re
from .errors import Syntax


def _add(a, b):
    return a + b

def _sub(a, b):
    return a - b

def _multi(a, b):
    return a * b

def _divide(a, b):
    return a / b

def _exp(a, b):
    return a ** b


_operation = {
    '+': _add,
    '-': _sub,
    '*': _multi,
    '/': _divide,
    '^': _exp
}

"""
Order of Operations:
    - Parentheses
    - Exponents
    - * and /
    - + and -
"""
_order = (
    ('^',),
    ('*', '/'),
    ('+', '-')
)


def solve(expression):
    # TODO: Test everything out with bad syntax.
    split = re.split("(\d*\.\d*|\d*)", expression)
    split = [x for x in split if x != "" and x != " "]

    while '(' in split:
        try:
            a, b = split.index('('), split.index(')')
        except ValueError:
            raise Syntax("Missing ')'")

        if split[a-1] not in _operation and a != 0:
            split = split[:a] + ["*"] + split[a:]
            a, b = split.index('('), split.index(')')

        try:
            if split[b+1] not in _operation:
                split = split[:b+1] + ["*"] + split[b+1:]
                a, b = split.index('('), split.index(')')
        except IndexError:
            pass

        split[b] = _calculate(split[a+1:b])
        split = split[:a] + split[b:]

    return _calculate(split)

def _calculate(split):
    print(f"--   {split}")
    if split[0] == '-':
        split = [0] + split
    order = 0
    changed = False
    while len(split) != 1:
        for k, value in enumerate(split):
            if value in _operation and value in _order[order]:
                changed = True
                # TODO: create error when a = -1 and when b is over len(split)
                a = float(split[k - 1])
                b = float(split[k + 1])

                new_value = _operation[value](a, b)
                print(f"{a} {value} {b} = {new_value}")

                split[k] = new_value
                split.pop(k+1)
                split.pop(k-1)
                print(f"--   {split}")

                # TODO: Might not need to break, could move the if changed to the for loop
                break
        if not changed:
            order += 1
            if order > len(_order):
                # raise UnknownSymbol(f"{self.expression} - Unknown Symbol, ({split})")
                raise Syntax(f"Either unsupported symbol or Syntax error.")
        else:
            changed = False

    # TODO: Round this / remove the .0 at the end
    return split[0]


# math_strings = ["5 + 5(2) - 3", "10 - 3(4)", "20 + 20(2)"]
# for math_string in math_strings:
#     print(math_string + "\n")
# math_string = "2^2^2^2"
# print(f"\n{math_string} = {solve(math_string)}")
# print("------------------------------------------\n")
