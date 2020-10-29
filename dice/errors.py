class Syntax(Exception):
    """
    Is raised when there is a Syntax error.
    Basically, when the user input it incorrectly / it doesn't know what the user wants
    """
    pass


class ArgumentRequired(Exception):
    """
    When the user input a command but the argument is missing.
    """
    pass
