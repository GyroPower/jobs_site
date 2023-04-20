from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="backend/templates")

home_router = APIRouter()

@home_router.get("/")
async def home(request:Request):
    return templates.TemplateResponse("general_pages/home_page.html",{"request":request})