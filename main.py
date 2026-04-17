from fastapi import FastAPI

from app.api.v1.router import router
from contextlib import asynccontextmanager
from app.core.database import engine
from app.models.models import User, Order, AdditionalWork
from app.models.service import Service, Photo
from app.models.base import Base

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=[User.__table__,
                                                              Order.__table__,
                                                              AdditionalWork.__table__,
                                                              Service.__table__,
                                                              Photo.__table__])
    yield
    await engine.dispose()

app = FastAPI(
    title='Customer Service API',
    version='1.0b',
    redoc_url='/redoc',
    docs_url='/docs',
    lifespan=lifespan
)
app.include_router(router)

from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8085)
