from sqlite3 import IntegrityError
from typing import Annotated
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Path, Body
from models import  Departments, Employees
from schemas.department import DepartmentCreate, DepartmentRead
from database import DBSessionDep
from schemas.department import DepartmentUpdate
from schemas.employee import EmployeeRead
router = APIRouter(prefix='/department', tags=['Отдел'])

@router.post('/add')
async def add_department(session: DBSessionDep,
                       data: Annotated[DepartmentCreate,
                                                Body()]
                      ) -> DepartmentRead | None:
    db_model = Departments(
        title = data.title,
        description = data.description
    )
    if not db_model:
        raise HTTPException(status_code=404, detail="Department not found")

    session.add(db_model)
    await session.commit()
    await session.refresh(db_model)
    return db_model

@router.get('/{id}')
async def get_department(session: DBSessionDep,
                       id: Annotated[int, Path(ge=0)]) -> None | DepartmentRead:
    result = await session.execute(
        select(Departments).where(Departments.id == id).limit(1)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Department not found")
    response = result.scalar_one_or_none()
    if not response:
        raise HTTPException(status_code=404, detail="Department not found")

    return response

@router.patch('/{id}')
async def update_department(
    session: DBSessionDep,
    id: Annotated[int, Path(ge=0)],
    update_data: DepartmentUpdate
) -> DepartmentRead:
    query = select(Departments).where(Departments.id == id)
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
async def delete_department(session: DBSessionDep,
                       id: Annotated[int, Path(ge=0)]):
    result = await session.execute(
        select(Departments).where(Departments.id == id).limit(1)
    )
    if not result:
        raise HTTPException(status_code=404, detail="Department not found")
    response = result.scalar_one_or_none()
    try:
        await session.delete(response)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Нельзя удалить: в отделе есть сотрудники или должности")

@router.get('/{id}/employees')
async def get_employees_by_department(
    session: DBSessionDep,
    id: Annotated[int, Path(ge=0)]
) -> list[EmployeeRead]:
    job_result = await session.execute(select(Departments).where(Departments.id == id))
    if not job_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Должность не найдена")

    query = select(Employees).where(Employees.department_id == id)
    result = await session.execute(query)
    employees = result.scalars().all()
    
    return employees
