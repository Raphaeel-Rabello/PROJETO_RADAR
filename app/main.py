from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import Base, engine
from app import models

from app.routers import (
    dashboard,
    opportunities,
    users,
    auth,
    plans
)


# Criação das tabelas do banco
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="RADAR",
    description="Inteligência em oportunidades",
    version="1.0.0"
)


# Rotas da API
app.include_router(dashboard.router)
app.include_router(opportunities.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(plans.router)


# Arquivos da interface
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/", include_in_schema=False)
def read_root():
    return FileResponse("static/index.html")