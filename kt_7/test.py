import os
from dotenv import load_dotenv

import pytest
import allure
import pytest_asyncio
from aiohttp import ClientResponseError

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.models import DogImg
from src.tasks import get_random_breed_img, get_post_by_id, insert_dog, compare_result_fc_get_post


@allure.feature("aiohttp")
class TestHttp:
    @pytest.mark.asyncio
    @allure.story("Task 1")
    @pytest.mark.parametrize("breed", ["spitz", "akita", "borzoi", "chow", "boxer",])
    async def test_async_fc(self, event_loop, breed: str):
        with allure.step("get json response"):
            json = await get_random_breed_img(breed)

        with allure.step("check success status"):
            assert json['status'] == 'success'

    @pytest.mark.asyncio
    @allure.story("Task 2")
    @pytest.mark.parametrize("post_id", ["q", "w", "e", "r", "t", "y"])
    async def test_invalid_request(self, event_loop, post_id: str):
        with allure.step("get 404 status code"):
            with pytest.raises(ClientResponseError, match="Not Found"):
                await get_post_by_id(post_id)

    @pytest.mark.asyncio
    @allure.story("Task 3")
    @pytest.mark.parametrize("breed", ["spit", "akit", "borzo", "cho", "boxe",])
    async def test_valid_request(self, event_loop, breed: str):
        with allure.step("get json response"):
            json = await get_random_breed_img(breed)

        with allure.step("check error status"):
            assert json['status'] == 'error'

        with allure.step("check status code"):
            assert json['code'] == 404

    @pytest.mark.asyncio
    @allure.story("Task 5")
    async def test_future_func(self, event_loop):
        with allure.step("start compare_result_fc_get_post func"):
            result = await compare_result_fc_get_post(1)

        with allure.step("check the result is true"):
            assert result


@allure.feature("asyncpg")
class TestDB:
    @pytest_asyncio.fixture()
    async def async_session(self):
        load_dotenv()
        engine = create_async_engine(os.getenv("ASYNC_DB_URL"), echo=True)

        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with async_session() as session:
            async with session.begin():
                yield session

        await engine.dispose()

    @pytest.mark.asyncio
    @allure.story("Task 4")
    @pytest.mark.parametrize("breed,img", [
        ("spitz", "spitz.png"),
        ("akita", "akita.png"),
        ("borzoi", "borzoi.png"),])
    async def test_async_db(self, event_loop, async_session, breed: str, img: str):
        with allure.step("insert dog img in postgres"):
            id = await insert_dog(async_session, breed, img)

        with allure.step("check row record exists by id"):
            assert await async_session.get(DogImg, id)
