from typing import Annotated
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Path, Body
from models import Employees
from schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from database import DBSessionDep
router = APIRouter(prefix='/employees', tags=['Сотрудник'])

@router.post('/add')
async def add_employee(session: DBSessionDep,
                       employee_data: Annotated[EmployeeCreate,
                                                Body()]
                      ) -> EmployeeRead | None:
    db_model = Employees(
        first_name = employee_data.first_name,
        last_name =employee_data.last_name,
        department_id =employee_data.department_id,
        job_title_id =employee_data.job_title_id,
        salary= employee_data.salary
    )
    session.add(db_model)
    await session.commit()
    await session.refresh(db_model)
    return db_model

@router.get('/all')
async def get_all_employees(
    session: DBSessionDep
) -> list[EmployeeRead]:
    result = await session.execute(select(Employees))
    employees = result.scalars().all()
    
    return employees


@router.get('/{id}')
async def get_employee(session: DBSessionDep,
                       id: Annotated[int, Path(ge=1)]) -> None | EmployeeRead:
    result = await session.execute(
        select(Employees).where(Employees.id == id).limit(1)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Department not found")
    response = result.scalar_one_or_none()

    return response

@router.patch('/{id}')
async def update_employee(
    session: DBSessionDep,
    id: Annotated[int, Path(ge=0)],
    update_data: EmployeeUpdate
) -> EmployeeRead:
    query = select(Employees).where(Employees.id == id)
    result = await session.execute(query)
    db_model = result.scalar_one_or_none()

    if not db_model:
        raise HTTPException(status_code=404, detail="Department not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_model, key, value)

    session.add(db_model)
    await session.commit()
    await session.refresh(db_model)

    return db_model

@router.delete('/{id}', status_code=204)
async def delete_employee(session: DBSessionDep,
                       id: Annotated[int, Path(ge=1)]):
    result = await session.execute(
        select(Employees).where(Employees.id == id).limit(1)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Department not found")
    response = result.scalar_one_or_none()
    await session.delete(response)
    await session.commit()
    return