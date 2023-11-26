import asyncio
import aiohttp
from typing import Coroutine

from sqlalchemy import insert

from models import DogImg


# Task 1, 3
async def get_random_breed_img(breed: str) -> Coroutine:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://dog.ceo/api/breed/{breed}/images/random') as resp:
            return await resp.json()


# Task 2
async def get_post_by_id(post_id: str | int) -> Coroutine | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}') as resp:
            resp.raise_for_status()
            return await resp.json()


# Task 4
async def insert_dog(async_session, breed: str, img: str) -> int:
    result = await async_session.execute(
        insert(DogImg).values(breed=breed, img=img)
    )
    return result.inserted_primary_key[0]


# Task 5
async def compare_result_fc_get_post(id: int | str,) -> bool:
    "Comparing the results of calling async func 'get_post_by_id' in different threads."
    loop = asyncio.get_running_loop()

    future = asyncio.run_coroutine_threadsafe(get_post_by_id(id), loop)
    await asyncio.sleep(2)
    future_result = future.result()

    result = await get_post_by_id(id)

    return future_result == result
