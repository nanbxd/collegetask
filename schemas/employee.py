from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class EmployeeCreate(BaseModel):
    first_name: str = Field(max_length = 20, min_length = 2)
    last_name: str = Field(max_length = 20, min_length = 2)
    department_id: int = Field(ge=1)
    job_title_id: int = Field(ge=1)
    salary: Decimal

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(max_length = 20, min_length = 2, default= None)
    last_name: Optional[str] = Field(max_length = 20, min_length = 2, default= None)
    department_id: Optional[int]
    job_title_id: Optional[int]
    salary: Optional[Decimal] = Field(ge=0)

class EmployeeRead(EmployeeCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)