from fastapi import FastAPI
from database import start_db
from routers.employees import router as employeesrout
from routers.departments import router as departmentrout
from routers.job_titles import router as job_titlerout

async def lifespan(app: FastAPI):
    await start_db()
    yield

app = FastAPI(title='Service', lifespan=lifespan)
app.include_router(employeesrout)
app.include_router(departmentrout)
app.include_router(job_titlerout)

@app.get('/')
async def status():
    return {'message': True}