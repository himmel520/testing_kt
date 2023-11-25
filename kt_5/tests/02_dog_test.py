import allure
import pytest

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import InternalError

from models import Dog, Nursery


@allure.feature("Dogs table")
class TestDog:
    @pytest.fixture
    def dogs(self) -> list[dict]:
        return [
            {"name": "Charlie", "image": "charlie_image.jpg",
                "breed": "Labrador Retriever", "subbreed": "", "nurseries_fk": 4},
            {"name": "Bella", "image": "bella_image.jpg",
                "breed": "German Shepherd", "subbreed": "", "nurseries_fk": 4},
            {"name": "Max", "image": "max_image.jpg", "breed": "Dachshund",
                "subbreed": "Miniature", "nurseries_fk": 4},
            {"name": "Lucy", "image": "lucy_image.jpg",
                "breed": "Golden Retriever", "subbreed": "", "nurseries_fk": 4},
            {"name": "Mia", "image": "mia_image.jpg",
                "breed": "Siberian Husky", "subbreed": "", "nurseries_fk": 4},
        ]

    @allure.story("Inserting dogs")
    @pytest.mark.parametrize("name,image,breed,subbreed,nursery_fk", [
        ("Lucy", "lucy_image.jpg", "Golden Retriever", "", 1),
        ("Max", "max_image.jpg", "Dachshund", "Miniature", 4),
        ("Mia", "mia_image.jpg", "Siberian Husky", "", 1),
    ])
    def test_insert(self, db_session, name: str, image: str, breed: str, subbreed: str, nursery_fk):
        with allure.step("insert dog in postgres"):
            stmt = insert(Dog).values(name=name, image=image,
                                      breed=breed, subbreed=subbreed, nurseries_fk=nursery_fk)
            result = db_session.execute(stmt)

        with allure.step("check len of a pk tuple"):
            assert len(pk := result.inserted_primary_key) == 1

        with allure.step("check row record exists by id"):
            assert db_session.get(Dog, pk[0])

    @allure.story("Updating dogs")
    @pytest.mark.parametrize("id,new_img", [
        (1, "lucy_image.jpeg"),
        (2, "max_image.png"),])
    def test_update(self, db_session, id: int, new_img: str):
        with allure.step("update dog in postgres"):
            stmt = update(Dog).where(Dog.id == id).values(image=new_img)
            db_session.execute(stmt)

        with allure.step("check correctness of city by id"):
            assert db_session.get(Dog, id).image == new_img

    @allure.story("Selecting dogs")
    @pytest.mark.parametrize("nursery_id,count", [(1, 2), (4, 1)])
    def test_select_by_nursery_id(self, db_session, nursery_id: int, count: int):
        with allure.step("select dogs in postgres by nursery_id"):
            stmt = select(Dog).join(Nursery, Dog.nurseries_fk ==
                                    Nursery.id).where(Nursery.id == nursery_id)
            result = db_session.execute(stmt).all()

        with allure.step("check count of dogs in nursery"):
            assert len(result) == count

    @allure.story("Deleting dogs")
    def test_delete(self, db_session):
        with allure.step("delete dog in postgres by id=3"):
            stmt = delete(Dog).where(Dog.id == 3)
            db_session.execute(stmt)

        with allure.step("check deleted dog by id=3"):
            assert not db_session.get(Dog, 3)

    @allure.story("Dogs limit constraint")
    def test_dogs_limit_constraint(self, db_session, dogs: list[dict]):
        with allure.step("create insert statment for dogs limit constraint"):
            stmt = insert(Dog).values(dogs)

        with allure.step("catch error from db"):
            with pytest.raises(InternalError, match="can not have more than 5 dogs in a nursery"):
                db_session.execute(stmt)
