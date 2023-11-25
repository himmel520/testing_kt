import os
from dotenv import load_dotenv

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


load_dotenv()


@pytest.fixture(scope='session', autouse=True)
def db_session():
    engine = create_engine(os.getenv("DATABASE_URL"))
    with Session(engine) as session:
        yield session
        session.commit()
