import json
import time
import pytest
import allure
from faker import Faker
from src.base_request import BaseRequest

fake = Faker()


@allure.feature("Profile Endpoint")
class TestProfile:
    @pytest.fixture
    def req(self):
        return BaseRequest(
            url="http://localhost:3000/profile",
            headers={
                'Content-Type': 'application/json'
            }
        )

    @allure.story("Get Profile")
    def test_get_profile(self, req):
        with allure.step("Sending GET request to retrieve profile"):
            res = req.get("", "")

        with allure.step("Verifying response"):
            assert res['status_code'] == 200
            assert len(res['json']) != 0

    @allure.story("Create Profile")
    @pytest.mark.parametrize(
        "name",
        [fake.user_name() for _ in range(5)])
    def test_create_profile(self, name, req):
        with allure.step("Creating a profile with name"):
            body = json.dumps({"name": name})
            res = req.post("", "", body)
            time.sleep(0.01)

        with allure.step("Verifying response"):
            assert res['status_code'] == 201
            assert "name" in res['json']

    @allure.story("Update Profile")
    @pytest.mark.parametrize(
        "name",
        [fake.user_name() for _ in range(5)])
    def test_update_profile(self, name, req):
        with allure.step("Updating profile with name"):
            body = json.dumps({"name": name})
            res = req.put("", "", body)
            time.sleep(0.01)

        with allure.step("Verifying response"):
            assert res['status_code'] == 200
            assert res['json']['name'] == name
