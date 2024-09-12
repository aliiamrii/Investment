from pydantic import BaseModel, constr

class UserCreateSchema(BaseModel):
    username: constr(min_length=4, max_length=80)
    password: constr(min_length=6, max_length=255)

    class Config:
        orm_mode = True
