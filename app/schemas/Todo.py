from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="Title must be between 3 and 100 characters")
    description: str = Field(min_length=3, description="Description must be greater than 3 characters")
    priority: int = Field(gt=0, lt=6)
    complete: bool