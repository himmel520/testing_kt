import os
import sys

import pytest
import allure

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import InternalError

from models import Buyer, Dog


@allure.feature("Buyers table")
class TestBuyer:
    @allure.story("Inserting buyers")
    @pytest.mark.parametrize("first_name,last_name,preferred_breeds", [
        ("Ivan", "Ivanov", "Labrador,German Shepherd,Siberian Husky"),
        ("Maria", "Petrova", "Golden Retriever,Poodle"),
        ("Alexey", "Smirnov", "Dachshund"),
    ])
    def test_insert(self, db_session, first_name: str, last_name: str, preferred_breeds: str):
        with allure.step("insert buyer in postgres"):
            stmt = insert(Buyer).values(first_name=first_name,
                                        last_name=last_name, preferred_breeds=preferred_breeds)
            result = db_session.execute(stmt)

        with allure.step("check row record exists by id"):
            assert db_session.get(Buyer, result.inserted_primary_key[0])

    @allure.story("Updating buyers")
    @pytest.mark.parametrize("id,dogs_fk", [
        (1, 2),
        (2, 1),
    ])
    def test_update(self, db_session, id: int, dogs_fk: int):
        with allure.step("update dogs_fk in buyer"):
            stmt = update(Buyer).where(Buyer.id == id).values(dogs_fk=dogs_fk)
            db_session.execute(stmt)

        with allure.step("check correctness of dogs_fk by id"):
            assert db_session.get(Buyer, id).dogs_fk == dogs_fk

    @allure.story("Selecting buyers")
    @pytest.mark.parametrize("name,dogs_fk", [
        ("Ivan", 2),
        ("Maria", 1),
        ("Alexey", None)
    ])
    def test_select(self, db_session, name: str, dogs_fk: int | None):
        with allure.step("select buyers in postgres by name"):
            stmt = select(Buyer).where(Buyer.first_name == name)
            result = db_session.execute(stmt).fetchone()[0]

        with allure.step("check dogs_fk by buyer's name"):
            assert result.dogs_fk == dogs_fk

    @allure.story("Deleting buyers")
    @pytest.mark.parametrize("id", [(2,), (3,)])
    def test_delete(self, db_session, id: int):
        with allure.step("delete buyer in postgres by id"):
            stmt = delete(Buyer).where(Buyer.id == id)
            db_session.execute(stmt)

        with allure.step("check deleted buyer by id"):
            assert not db_session.get(Buyer, id)

    @allure.story("Preferred dogs constraint")
    @pytest.mark.parametrize("first_name,last_name,preferred_breeds", [("Ivan", "Ivanov", "Labrador,German Shepherd,Siberian Husky, 4"),])
    def test_preferred_dogs_constraint(self, db_session, first_name: str, last_name: str, preferred_breeds: str):
        with allure.step("insert buyer in postgres"):
            stmt = insert(Buyer).values(first_name=first_name,
                                        last_name=last_name, preferred_breeds=preferred_breeds)

        with allure.step("catch error from db"):
            with pytest.raises(InternalError, match="Exceeded limit of preferred breeds"):
                db_session.execute(stmt)
