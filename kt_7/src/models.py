from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class DogImg(Base):
    __tablename__ = 'dogs_img'

    id: Mapped[int] = mapped_column(primary_key=True)
    breed: Mapped[str] = mapped_column(String(100))
    img: Mapped[str]

    def __repr__(self):
        return f"Dog(id={self.id}, breed={self.breed}, img={self.img})"
