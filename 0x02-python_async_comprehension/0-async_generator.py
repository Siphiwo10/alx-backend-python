#!/usr/bin/env python3
"""Module"""


import asyncio
import random


async def async_generator():
    """module docs"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
