from typing import Optional

from sqlalchemy import ForeignKey, DDL, String
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class Base(DeclarativeBase):
    ...


class Dog(Base):
    __tablename__ = 'dogs'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    image: Mapped[str] = mapped_column(default='-')
    breed: Mapped[str] = mapped_column(String(100))
    subbreed: Mapped[str] = mapped_column(String(100))

    buyer: Mapped['Buyer'] = relationship(back_populates="dog", uselist=False)

    nursery: Mapped['Nursery'] = relationship(
        back_populates="dogs", uselist=False)
    nurseries_fk: Mapped[int] = mapped_column(
        ForeignKey('nurseries.id'), default=None)

    def __repr__(self):
        return f"Dog(id={self.id}, name={self.name}, breed={self.breed}, subbreed={self.subbreed})"


class Nursery(Base):
    __tablename__ = 'nurseries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))

    dogs: Mapped[list['Dog']] = relationship(
        back_populates="nursery", uselist=True)

    def __repr__(self):
        return f"Nursery(id={self.id}, name={self.name}, country={self.country}, city={self.city})"


class Buyer(Base):
    __tablename__ = 'buyers'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    preferred_breeds: Mapped[str]

    dog: Mapped['Dog'] = relationship(back_populates="buyer", uselist=False)
    dogs_fk: Mapped[Optional[int]] = mapped_column(
        ForeignKey('dogs.id'), nullable=True, default=None)

    def __repr__(self):
        return f"Buyer(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, preferred_breeds={self.preferred_breeds})"


def dogs_limit_trigger(target, connection, **kw) -> None:
    connection.execute(DDL("""
    CREATE OR REPLACE FUNCTION fc_check_dogs_limit()
    RETURNS TRIGGER AS $$
    BEGIN
        IF (SELECT COUNT(*) FROM dogs WHERE dogs.nurseries_fk = NEW.nurseries_fk) > 5 THEN
            RAISE EXCEPTION 'can not have more than 5 dogs in a nursery';
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER tg_check_dogs_limit
    BEFORE INSERT OR UPDATE
    ON dogs
    FOR EACH ROW
    EXECUTE FUNCTION fc_check_dogs_limit();
    """))


def preferred_breeds_limit_trigger(target, connection, **kw) -> None:
    connection.execute(DDL("""
    CREATE OR REPLACE FUNCTION fc_check_preferred_breeds_limit()
    RETURNS TRIGGER AS $$
    BEGIN
        IF (array_length(string_to_array(NEW.preferred_breeds, ','), 1) > 3) THEN
            RAISE EXCEPTION 'Exceeded limit of preferred breeds';
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER tg_check_preferred_breeds_limit
    BEFORE INSERT OR UPDATE
    ON buyers
    FOR EACH ROW
    EXECUTE FUNCTION fc_check_preferred_breeds_limit();
    """))
