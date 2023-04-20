from fastapi import APIRouter
from backend.apis.version1 import route_general_pages,route_users,route_jobs,auth

api_router=APIRouter()

api_router.include_router(router=route_general_pages.home_router,tags=["general_pages"])
api_router.include_router(router=route_users.users_router,prefix="/users",tags=['users'])
api_router.include_router(router=route_jobs.router,prefix="/jobs",tags=['jobs'])
api_router.include_router(router=auth.auth_router,prefix="/login",tags=["Login"])