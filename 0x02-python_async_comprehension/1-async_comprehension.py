#!/usr/bin/env python3
"""Import previous task"""


import asyncio


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension():
    """async comprehension"""
    random_numbers = [num async for num in async_generator()]
    return random_numbers
