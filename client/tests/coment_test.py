import json
import logging
import time
import pytest
import allure
from faker import Faker
from src.base_request import BaseRequest

fake = Faker()


@allure.feature("Comments Endpoint")
class TestComments:
    @pytest.fixture
    def req(self):
        return BaseRequest(
            url="http://localhost:3000/posts",
            headers={
                'Content-Type': 'application/json'
            }
        )

    @allure.story("Get comments by 1 post")
    def test_get_no_comments(self, req):
        with allure.step("Sending GET request to retrieve comments"):
            res = req.get("1", "comments")

        with allure.step("Verifying response"):
            assert res['status_code'] == 200
            assert len(res['json']) != 0

    @allure.story("Create comment")
    @pytest.mark.parametrize(
        "body",
        [fake.text(30) for i in range(5)])
    def test_create_comment(self, body, req):
        with allure.step(f"Creating a comment with body"):
            body = json.dumps({"body": body})
            res = req.post("1", "comments", body)
            time.sleep(0.01)

        with allure.step("Verifying response"):
            assert res['status_code'] == 201
            assert "postId" in res['json']
