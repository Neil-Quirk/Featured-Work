def left(s, amount):
    """
    Consumes a string (s) and returns (amount) characters from the left
    :param s: str - The string variable the function consumes
    :param amount: int - The number of characters
    :return: str - left indexed
    """
    return s.str[:amount]


def right(s, amount):
    """
    Consumes a string (s) and returns (amount) characters from the Right
    :param s: str - The string variable the function consumes
    :param amount: int - The number of characters
    :return: str - Right indexed
    """
    return s.str[-amount:]
