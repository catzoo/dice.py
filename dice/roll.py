import re
from .dice import *
from .py_math import solve as math_solve
from .errors import ArgumentRequired


def _roll_dice(_, number, sides):
    if number is None:
        number = 1
        position = (0, 1)
    else:
        position = (-1, 1)

    if sides == 'f':
        dice = FateDice.roll(number)
    elif isinstance(sides, int):
        dice = Dice.roll(number, sides)
    else:
        raise ArgumentRequired("Sides is required for 'd'")

    return dice, position


def _compare_dice(dice, compare, number):
    if number is None:
        raise ArgumentRequired("Need a number to compare")

    if compare == "<=" or compare == "=<":
        dice.le(number)

    elif compare == ">=" or compare == "=>":
        dice.ge(number)

    elif compare == ">":
        dice.gt(number)

    elif compare == "<":
        dice.lt(number)

    elif compare == "=":
        dice.eq(number)

    return dice, (0, 1)


_dice_operation = {
    # character: (method, (arguments,), (convert_to_types,))
    # -- note to self, there is a order in convert_to_types. If its (int, str), it'll try int first then str
    # -- so if its _roll_dice, int is more important since almost anything can be a str
    'd': (_roll_dice,
          (-1, 1),
          (int, (int, str))
          ),

    **dict.fromkeys(('>=', "<=", "=", "=>", "=<", "<", ">"),
                    (_compare_dice,
                     (0, 1),
                     (str, int)
                     )),
}

_regex = list(_dice_operation)
_regex.append("\d*\.\d*|\d*")
_regex_pattern = f"({'|'.join(_regex)})"


def _convert(argument, types):
    if not isinstance(types, tuple):
        types = (types,)

    for t in types:
        try:
            argument = t(argument)
            return argument
        except ValueError:
            pass

    return None

def roll(expression):
    original_expression = expression
    expression = expression.lower()
    expression = re.split(_regex_pattern, expression)
    # Cleaning it up
    expression = [x for x in expression if x != '' and x != ' ']

    index = 0
    dices_values = []
    dices_strings = []
    while True:
        dice, replace, expression = _roll(expression)
        if dice:
            dices_values.append(f"({dice.value()})")
            dices_strings.append(f"({dice})")
            expression[replace] = "{" + str(index) + "}"
            index += 1
        else:
            break

    expression = ' '.join(expression)
    math_expression = expression.format(*dices_values)
    user_expression = expression.format(*dices_strings)

    end_value = math_solve(math_expression)

    return f"`{original_expression}` = {user_expression} = {end_value}"

def _roll(expression):
    remove = []
    dice = None
    changed = None
    return_index = None
    k = 0
    while k < len(expression):
        v = expression[k]

        if v in _dice_operation:
            v = _dice_operation[v]

            arguments = [x for x in range(len(v[1]))]

            for x in arguments:
                a = k + v[1][x]
                if 0 <= a < len(expression):
                    arguments[x] = _convert(expression[a], v[2][x])
                else:
                    arguments[x] = None

            # Running the method
            dice, position = v[0](dice, *arguments)
            # Marking it to be removed. This should add something similar to [0, 1, 2] to the remove list
            remove += list(range(k + position[0], k + position[1] + 1))

            changed = True
            k += position[1]

        if changed:
            changed = False
        elif changed is False:
            # change can be None, so making sure its False
            break

        k += 1

    if remove:
        return_index = remove[0]

        remove.pop(0)  # using the first index to replace it
        remove.reverse()

        for k in remove:
            expression.pop(k)

    return dice, return_index, expression
