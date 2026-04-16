from fastapi import FastAPI

from api import router
from contextlib import asynccontextmanager
from core.database import engine
from models import Base, models, service

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=[models.User.__table__,
                                                              models.Order.__table__,
                                                              models.AdditionalWork.__table__,
                                                              service.Service.__table__,
                                                              service.Photo.__table__])
    yield
    await engine.dispose()

app = FastAPI(title='Customer Service API',
              version='1.0b',
              root_path="/v1",
              redoc_url='/',
              docs_url=None,
              lifespan=lifespan
              )
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8085)
