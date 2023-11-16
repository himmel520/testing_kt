import json
import logging

from src.store import store_request
from src.user import user_request


BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(funcName)s %(message)s"
    )

    store_request(BASE_URL_PETSTORE)
    user_request(BASE_URL_PETSTORE)


if __name__ == "__main__":
    main()
