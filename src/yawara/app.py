from fastapi import FastAPI

from yawara.routers import auth, usuarios

app = FastAPI(
  title="Yawara",
  docs_url="/docs",
  redoc_url=None,
  openapi_url="/openapi.json",
)

app.include_router(auth.router)
app.include_router(usuarios.router)
