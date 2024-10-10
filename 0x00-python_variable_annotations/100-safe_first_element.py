#!/usr/bin/env python3
"""making first elements seq"""


from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    if lst:
        return lst[0]
    else:
        return None

