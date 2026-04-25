from sqlite3 import IntegrityError
from typing import Annotated
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Path, Body
from models import  Job_titles
from schemas.job_title import Job_titleCreate, Job_titleRead, Job_titleUpdate
from models import Employees
from schemas.employee import EmployeeRead  
from database import DBSessionDep
router = APIRouter(prefix='/job_title', tags=['Должность'])

@router.post('/add')
async def add_job_title(session: DBSessionDep,
                       data: Annotated[Job_titleCreate,
                                                Body()]
                      ) -> Job_titleRead | None:
    db_model = Job_titles(
        department_id = data.department_id,
        title = data.title,
        description = data.description
    )
    session.add(db_model)
    await session.commit()
    await session.refresh(db_model)
    return db_model

@router.get('/{id}')
async def get_job_title(session: DBSessionDep,
                       id: Annotated[int, Path(ge=1)]) -> None | Job_titleRead:
    result = await session.execute(
        select(Job_titles).where(Job_titles.id == id).limit(1)
    )
    response = result.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Должность не найдена")

    return response
@router.patch('/{id}')
async def update_job_title(
    session: DBSessionDep,
    id: Annotated[int, Path(ge=0)],
    update_data: Job_titleUpdate
) -> Job_titleRead:
    query = select(Job_titles).where(Job_titles.id == id)
    result = await session.execute(query)
    db_model = result.scalar_one_or_none()

    if not db_model:
        raise HTTPException(status_code=404, detail="Job_title not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_model, key, value)

    session.add(db_model)
    await session.commit()
    await session.refresh(db_model)

    return db_model

@router.delete('/{id}', status_code=204)
async def delete_job_title(session: DBSessionDep,
                       id: Annotated[int, Path(ge=0)]):
    result = await session.execute(
        select(Job_titles).where(Job_titles.id == id).limit(1)
    )
    response = result.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=404, detail="Должность не найдена")
    try:
        await session.delete(response)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Нельзя удалить: в данной должности числятся сотрудники")
    return



@router.get('/{id}/employees')
async def get_employees_by_job_title(
    session: DBSessionDep,
    id: Annotated[int, Path(ge=1)]
) -> list[EmployeeRead]:
    job_result = await session.execute(select(Job_titles).where(Job_titles.id == id))
    if not job_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Должность не найдена")

    query = select(Employees).where(Employees.job_title_id == id)
    result = await session.execute(query)
    employees = result.scalars().all()
    
    return employees
