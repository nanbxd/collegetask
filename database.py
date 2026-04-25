from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from base import Base
from models import Employees, Departments, Job_titles

engine =  create_async_engine(url='sqlite+aiosqlite:///./mydb.db')
new_session = async_sessionmaker(engine, 
                              expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

DBSessionDep = Annotated[AsyncSession, Depends(get_session)]