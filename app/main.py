from fastapi import FastAPI

from api.v1.router import router


app = FastAPI(title='Customer Service API',
              version='1.0b',
              root_path="/v1",
              redoc_url='/',
              docs_url=None,
              )
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8085)
