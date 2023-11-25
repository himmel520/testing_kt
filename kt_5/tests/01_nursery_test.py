import allure
import pytest

from sqlalchemy import delete, insert, select, update

from models import Nursery


@allure.feature("Nurseries table")
class TestNursery:
    @allure.story("Inserting 3 nurseries")
    @pytest.mark.parametrize("name,country,city", [
        ("Russian Paws", "Russia", "Moscow"),
        ("Siberian Tails", "Russia", "St. PetersburgSt."),
        ("Golden Hearts", "Russia", "Kaliningrad"),
        ("Glamour Zapada", "Russia", "Kaliningrad"),])
    def test_insert(self, db_session, name: str, country: str, city: str):
        with allure.step("insert nursery in postgres"):
            stmt = insert(Nursery).values(
                name=name, country=country, city=city)
            result = db_session.execute(stmt)

        with allure.step("check len of a pk tuple"):
            assert len(pk := result.inserted_primary_key) == 1

        with allure.step("check row record exists by id"):
            assert db_session.get(Nursery, pk[0])

    @allure.story("Updating nurseries")
    @pytest.mark.parametrize("id,city", [
        (1, "Novosibirsk"),
        (2, "Nizhny Novgorod"),
        (3, "Kazan"),
    ])
    def test_update(self, db_session, id: int, city: str):
        with allure.step("update nursery in postgres"):
            stmt = update(Nursery).where(Nursery.id == id).values(city=city)
            db_session.execute(stmt)

        with allure.step("check correctness of city by id"):
            assert db_session.get(Nursery, id).city == city

    @allure.story("Selecting nurseries")
    @pytest.mark.parametrize("id,name,country,city", [
        (1, "Russian Paws", "Russia", "Novosibirsk"),
        (2, "Siberian Tails", "Russia", "Nizhny Novgorod"),
        (3, "Golden Hearts", "Russia", "Kazan"),])
    def test_select(self, db_session, id: int, name: str, country: str, city: str):
        with allure.step("select nursery in postgres by id"):
            stmt = select(Nursery).where(Nursery.id == id)
            result = db_session.execute(stmt).fetchone()[0]

        with allure.step("check correctness of nursery data"):
            assert result.name == name and result.country == country and result.city == city

    @allure.story("Deleting nurseries")
    @pytest.mark.parametrize("id", [(2,), (3,)])
    def test_delete(self, db_session, id: int):
        with allure.step("delete nursery in postgres by id"):
            stmt = delete(Nursery).where(Nursery.id == id)
            db_session.execute(stmt)

        with allure.step("check deleted nursery by id"):
            assert not db_session.get(Nursery, id)
