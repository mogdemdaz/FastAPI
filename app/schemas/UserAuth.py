from pydantic import Field, BaseModel


class UserAuth(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)
