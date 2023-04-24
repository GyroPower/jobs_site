from fastapi import APIRouter

from backend.webapss.auth.route_auth import router as auth_app
from backend.webapss.jobs.route_jobs import router as jobs_app
from backend.webapss.users.route_users import router as users_app

apps_router = APIRouter()

apps_router.include_router(
    router=jobs_app, prefix="", tags=["Jobs"], include_in_schema=False
)
apps_router.include_router(router=users_app, prefix="", tags=["Users"])
apps_router.include_router(router=auth_app, prefix="", tags=["Auth"])
