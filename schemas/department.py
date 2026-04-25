from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class DepartmentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=20)
    description: str = Field(min_length=2, max_length=500)
class DepartmentUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=20)
    description: Optional[str] = Field(default= None, min_length=10, max_length=500)

class DepartmentRead(DepartmentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)