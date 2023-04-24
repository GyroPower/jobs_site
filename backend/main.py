from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .apis.base import api_router as apis_router
from .apis.version1.route_auth import auth_router
from .core.config import settings
from .db.base import Base
from .db.database import engine
from .webapss.base import apps_router

# to get a random secret_key run this command in linux:
# openssl rand -hex 32


def include_routers(app: FastAPI):
    app.include_router(apis_router)
    app.include_router(apps_router)


def conf_static(app: FastAPI):
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_app():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_routers(app)
    conf_static(app)
    create_tables()
    return app


start_app()
