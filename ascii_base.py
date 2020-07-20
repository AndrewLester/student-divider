import string
from typing import AnyStr, List, Union


def float_to_letters(num: float, precision: int, letters: str = string.ascii_uppercase) -> str:
    return _float_to_letters(num, 26, letters, precision)


def _int_to_base(number: int, new_base: int, symbols: Union[AnyStr, List[str]]):
    # Uses "the division method"
    sign = -1 if number < 0 else 1
    number *= sign
    ans = ''
    while number:
        ans += symbols[number % new_base]
        number //= new_base
    if sign == -1:
        ans += '-'
    return ans[::-1]


def _float_to_letters(num: float, new_base: int, symbols: Union[AnyStr, List[str]], precision: int = None, ):
    integral, _, fractional = str(num).strip().partition('.')
    num = int(integral + fractional, 10) * 10 ** -len(fractional)

    #to new_base
    precision = len(fractional) if precision is None else precision
    s = _int_to_base(int(round(num / new_base ** -precision)), new_base, symbols)
    if precision:
        return s[:-precision] + s[-precision:].lower()
    else:
        return s
