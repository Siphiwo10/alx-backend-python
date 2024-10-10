#!/usr/bin/env python3
"""annotated function sum_mixed_list which takes a list mxd_lst"""


from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Return the sum of integers and floats in a mixed list."""
    return sum(mxd_lst)
