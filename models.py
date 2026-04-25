from decimal import Decimal
from base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BIGINT, ForeignKey, String, Numeric

class Employees(Base):
    __tablename__ = 'employees'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    job_title_id: Mapped[int] = mapped_column(ForeignKey('job_titles.id'))
    salary: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=2), nullable=True)

    department: Mapped["Departments"] = relationship(back_populates="employees")
    job_title: Mapped["Job_titles"] = relationship(back_populates="employees")

class Departments(Base):
    __tablename__ = 'departments'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(500))
    employees: Mapped[list["Employees"]] = relationship(back_populates="department")
    job_titles: Mapped[list["Job_titles"]] = relationship(back_populates="department")

class Job_titles(Base):
    __tablename__ = 'job_titles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(500))
    employees: Mapped[list["Employees"]] = relationship(back_populates="job_title")

    department: Mapped["Departments"] = relationship(back_populates="job_titles")