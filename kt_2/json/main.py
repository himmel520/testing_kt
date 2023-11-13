import json
import logging

json_path = "json/data/SuperHero.json"
update_json_path = "json/data/update_SuperHero.json"


def read_json() -> dict:
    with open(json_path, encoding='utf-8') as f:
        return json.load(f)


def create_new_json(new_data: dict) -> None:
    with open(update_json_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4)


def add_new_members(data: dict, new_members: list[dict]) -> None:
    data["members"].extend(new_members)
    data["members"].sort(key=lambda member: len(
        member["powers"]), reverse=True)


def main() -> None:
    new_members = [
        {
            "name": "Captain Velocity",
            "age": 32,
            "secretIdentity": "Victor Swift",
            "powers": ["Super speed", "Invisibility", "Enhanced agility"]
        },
        {
            "name": "Tech Savvy",
            "age": 28,
            "secretIdentity": "Alex Bytes",
            "powers": ["Technological mastery", "Hacking skills", "Teleportation"]
        }
    ]
    try:
        data = read_json()
        add_new_members(data, new_members)
        create_new_json(data)
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
