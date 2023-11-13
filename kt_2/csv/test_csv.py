import pytest
from main import check_grade, change_csv_data


class TestCSV:
    @pytest.fixture
    def valid_data(self):
        return [
            ["John", "Doe", "123-45-6789", "90.0",
                "85.0", "88.0", "92.0", "80", "A"],
            ["Alice", "Smith", "123-45-689", "55.0",
                "45.0", "58.0", "54.0", "53", "C-"],
            ["Bob", "Smith", "123-45-679", "55.0",
                "0", "40", "30", "32", "F"],
        ]

    @pytest.fixture
    def invalid_data(self):
        return [
            ["John", "Doe", "123-45-6789", "90.0",
                "0", "88.0", "92.0", "80", "A"],
            ["Alice", "Smith", "123-45-689", "55.0",
                "45.0", "100.0", "54.0", "53", "C-"],
            ["Bob", "Smith", "123-45-679", "55.0",
                "0", "40", "32", "F"],
            ["Bob", "Smith", "123-45-679", "55.0",
                "0", "40,sd", "32", "F"],
        ]

    def test_change_csv_data_valid(self, valid_data):
        new_data = change_csv_data(valid_data)
        assert len(new_data) == 3

    def test_change_csv_data_invalid(self, invalid_data):
        new_data = change_csv_data(invalid_data)
        assert len(new_data) == 0

    @pytest.mark.parametrize("mean,grade", [
        (96.1, "A+"),
        (70, "B"),
        (1, "F"),
        (35, "D-"),])
    def test_check_valid_grade(self, mean, grade):
        assert check_grade(mean, grade)

    @pytest.mark.parametrize("mean,grade", [
        (111.1, "A+"),
        (9, "B"),
        (36, "F"),
        (0, "D-"),])
    def test_check_invalid_grade(self, mean, grade):
        assert not check_grade(mean, grade)
