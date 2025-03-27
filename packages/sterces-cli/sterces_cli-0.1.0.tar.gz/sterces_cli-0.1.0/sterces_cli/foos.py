"""Top level module foos from sterces-cli app package."""

from typing import Dict, List, Optional, Union

IntStrBool = Union[int, str, bool]
StrStrList = str | List[str]
StrIntStrBool = Dict[str, IntStrBool]
StrOptStr = Dict[str, Optional[str]]


def add_arg(sgrawk: StrOptStr, key: str, valor: Optional[StrStrList]) -> None:
    """Add an argument to a kwargs dictionary.

    :param sgrawk: kwargs dictionary
    :type sgrawk: dict[str, Optional[str]]
    :param key: argument key
    :type key: str
    :param valor: argument value
    :type valor: Optional[Union[str, list[str]]]
    """
    if isinstance(valor, list):
        sgrawk[key] = ", ".join(valor)
        return
    sgrawk[key] = valor


def add_arg_if(sgrawk: StrIntStrBool, key: str, valor: Optional[IntStrBool]) -> None:
    """Add a IntStrBool arg to a kwargs dictionary if it is not None, False, or empty.

    :param sgrawk: kwargs dictionary
    :type sgrawk: dict[str, Optional[str]]
    :param key: argument key
    :type key: str
    :param valor: argument value
    :type valor: Optional[Union[str, list[str]]]
    """
    if valor:
        sgrawk[key] = valor
