import os
from dotenv import load_dotenv

from sqlalchemy.inspection import inspect
from sqlalchemy import event, create_engine

from models import Base
from models import dogs_limit_trigger, preferred_breeds_limit_trigger


def main() -> None:
    """Creating tables and triggers in postgres"""

    load_dotenv()
    engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

    inspector = inspect(engine)
    if not inspector.get_table_names():
        event.listen(Base.metadata, 'after_create',
                     dogs_limit_trigger)
        event.listen(Base.metadata, 'after_create',
                     preferred_breeds_limit_trigger)
        Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
