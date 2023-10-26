from pydantic import BaseModel


class KeyValueSchema(BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True


class DeviderDevidentSchema(BaseModel):
    dividend: int
    divider: int

    class Config:
        orm_mode = True
