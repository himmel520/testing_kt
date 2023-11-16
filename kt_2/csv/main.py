import csv
import logging

CSV_PATH = "csv/data/grades.csv"
UPDATE_CSV_PATH = "csv/data/update_grades.csv"


def read_csv() -> list[list]:
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        return list(csv.reader(f))[1:]


def create_new_csv(new_rows: list[dict]) -> None:
    with open(UPDATE_CSV_PATH, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['full name', 'mean', 'grade'])
        writer.writeheader()
        writer.writerows(new_rows)


def change_csv_data(rows: list[list]) -> list[dict]:
    new_data = []
    for i, row in enumerate(rows):
        try:
            grades = [float(num) for num in row[3:-1] if float(num) >= 0]
            if len(grades) < 5:
                raise ValueError("all numbers must be positive")

            mean = sum(grades)/5
            if not check_grade(mean, grade=row[-1]):
                raise ValueError("invalid mean or garde")

            new_data.append({
                'full name': f"{row[0]} {row[1]}",
                'mean': mean,
                'grade': row[-1],
            })

        except ValueError as e:
            logging.warning(f"Error on row {i+2}: {e}")

    return new_data


def check_grade(mean: float, grade: str) -> bool:
    grades = {
        "A+": 90, "A": 85, "A-": 80,
        "B+": 75, "B": 70, "B-": 65,
        "C+": 60, "C": 55, "C-": 50,
        "D+": 45, "D": 40, "D-": 35,
        "F": 0
    }

    match grade:
        case "A+":
            increment = 11
        case "F":
            increment = 35
        case _:
            increment = 5

    return mean >= (num := grades.get(grade, 0)) and mean < num + increment


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    )

    new_data = change_csv_data(read_csv())
    create_new_csv(new_data)


if __name__ == "__main__":
    main()
