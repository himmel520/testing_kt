import pytest
import json


class TestJson:
    @pytest.fixture
    def files(self) -> tuple[dict]:
        with open("data/SuperHero.json") as f1, open("data/update_SuperHero.json") as f2:
            return json.load(f1), json.load(f2)

    def test_compare_json(self, files):
        assert files[0] != files[1]
