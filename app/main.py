from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.cats_crud import router as cats_router
from app.missions_crud import router as missions_router
from app.targets_crud import router as targets_router
from app.db import get_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Підключення роутерів для кожної групи ендпоінтів
app.include_router(cats_router, tags=["cats"])
app.include_router(missions_router, tags=["missions"])
app.include_router(targets_router, tags=["targets"])

