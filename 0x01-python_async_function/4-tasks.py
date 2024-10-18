#!/usr/bin/env python3
"""Take the code from wait_n and alter it into a new
function task_wait_n."""


import asyncio
from typing import List
from asyncio import Task


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """wait using n"""
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    return await asyncio.gather(*tasks)
