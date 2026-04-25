from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class Job_titleCreate(BaseModel):
    department_id: int = Field(ge=1)
    title: str = Field(min_length=2, max_length=20)
    description: str = Field(min_length=2, max_length=500)
class Job_titleUpdate(BaseModel):
    department_id: Optional[int] = Field(default=None, ge=1)
    title: Optional[str] = Field(default=None, min_length=2, max_length=20)
    description: Optional[str] = Field(default=None, min_length=10, max_length=500)
    
class Job_titleRead(Job_titleCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)