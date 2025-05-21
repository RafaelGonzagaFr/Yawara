from fastapi import FastAPI

from yawara.routers import auth, pets, servicos, usuarios
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
  title="Yawara",
  docs_url="/docs",
  redoc_url=None,
  openapi_url="/openapi.json",
)

# Permitir qualquer origem (DURANTE O DESENVOLVIMENTO APENAS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:5500"] em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(pets.router)
app.include_router(servicos.router)
