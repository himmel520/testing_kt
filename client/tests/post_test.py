import json
import time
import pytest
import allure
from faker import Faker
from src.base_request import BaseRequest

fake = Faker()


@allure.feature("Posts Endpoint")
class TestPosts:
    @pytest.fixture
    def req(self):
        return BaseRequest(
            url="http://localhost:3000/posts",
            headers={
                'Content-Type': 'application/json'
            }
        )

    @allure.story("Get Posts")
    def test_get_posts(self, req):
        with allure.step("Sending GET request to retrieve posts"):
            res = req.get("")

        with allure.step("Verifying response"):
            assert res['status_code'] == 200
            assert isinstance(res['json'], list)

    @allure.story("Create Post")
    @pytest.mark.parametrize(
        "title,author",
        [(fake.text(20), fake.name()) for _ in range(5)])
    def test_create_post(self, title, author, req):
        with allure.step(f"Creating a post with title: {title}, author: {author}"):
            body = json.dumps({"title": title, "author": author})
            res = req.post("", "", body)
            time.sleep(0.01)

        with allure.step("Verifying response"):
            assert res['status_code'] == 201
            assert "id" in res['json']

    @allure.story("Get Single Post")
    @pytest.mark.parametrize(
        "id",
        range(1, 6))
    def test_get_single_post(self, id, req):
        with allure.step(f"Sending GET request for post with id: {id}"):
            res = req.get(str(id), "")

        with allure.step("Verifying response"):
            assert res['status_code'] == 200

    @allure.story("Update Post")
    @pytest.mark.parametrize(
        "title,author,id",
        [(fake.text(20), fake.name(), i) for i in range(1, 6)])
    def test_update_post(self, title, author, id, req):
        with allure.step(f"Updating post with id: {id}, title: {title}, author: {author}"):
            body = json.dumps({"title": title, "author": author})
            res = req.put(str(id), "", body)
            time.sleep(0.01)

        with allure.step("Verifying response"):
            assert res['status_code'] == 200
            assert res['json']["id"] == id

    @allure.story("Delete Post")
    def test_delete_post(self, req):
        with allure.step("Sending DELETE request for post with id: 1"):
            res = req.delete("1", "")

        with allure.step("Verifying response"):
            assert res['status_code'] == 200
