from fastapi import APIRouter

from backend.apis.version1 import route_auth
from backend.apis.version1 import route_general_pages
from backend.apis.version1 import route_jobs
from backend.apis.version1 import route_users

api_router = APIRouter()

api_router.include_router(
    router=route_general_pages.home_router, tags=["general_pages"]
)
api_router.include_router(
    router=route_users.users_router, prefix="/users", tags=["users"]
)
api_router.include_router(router=route_jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(
    router=route_auth.auth_router, prefix="/login", tags=["Login"]
)
