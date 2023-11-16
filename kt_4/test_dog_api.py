import pytest
import allure
import httpx

from response_models import ResponseBreeds, ResponseImg, ResponseBreed


@allure.feature("Dog API")
class TestDogAPI:
    @allure.story("list all breeds")
    def test_all_breeds_list(self):
        with allure.step("get list"):
            r = httpx.get("https://dog.ceo/api/breeds/list/all")

        with allure.step("check status code"):
            assert r.status_code == 200

        with allure.step("check_json"):
            ResponseBreeds(**r.json())

    @allure.story("random img")
    def test_random_img(self):
        with allure.step("get img"):
            r = httpx.get("https://dog.ceo/api/breeds/image/random")

        with allure.step("check status code"):
            assert r.status_code == 200

        with allure.step("check_json"):
            ResponseImg(**r.json())

    @allure.story("all breed img")
    @pytest.mark.parametrize(
        "breed",
        ["borzoi", "chow", "spitz"])
    def test_breed(self, breed):
        with allure.step("get img"):
            r = httpx.get(f"https://dog.ceo/api/breed/{breed}/images")

        with allure.step("check status code"):
            assert r.status_code == 200

        with allure.step("check_json"):
            json_data = r.json()
            ResponseBreed(**json_data)
            assert all([breed in i for i in json_data["message"]])

    @allure.story("invalid all breed img")
    @pytest.mark.parametrize(
        "breed",
        ["asdfg", "", "sPiTz"])
    def test_invalid_breed(self, breed):
        with allure.step("get img"):
            r = httpx.get(f"https://dog.ceo/api/breed/{breed}/images")

        with allure.step("check invalid status code"):
            assert r.status_code == 404

    @allure.story("all sub breeds from a breed")
    @pytest.mark.parametrize(
        "breed",
        ["australian", "bulldog", "spitz"])
    def test_sub_breeds(self, breed):
        with allure.step(f"get all sub breeds from a {breed}"):
            r = httpx.get(f"https://dog.ceo/api/breed/{breed}/list")

        with allure.step("check status code"):
            assert r.status_code == 200

        with allure.step("check_json"):
            json_data = r.json()
            ResponseBreed(**json_data)
            assert len(json_data) > 0
