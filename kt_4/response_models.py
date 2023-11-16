from pydantic import BaseModel


class ResponseBreeds(BaseModel):
    message: dict
    status: str


class ResponseImg(BaseModel):
    message: str
    status: str


class ResponseBreed(BaseModel):
    message: list
    status: str
