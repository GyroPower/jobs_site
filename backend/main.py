from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .apis import base 
from .apis.version1.auth import auth_router
from fastapi.responses import HTMLResponse
from .core.config import settings
from .db.base import Base
from .db.database import engine
# to get a random secret_key run this command in linux:
# openssl rand -hex 32



def include_routers(app:FastAPI):
    app.include_router(base.api_router)
    
def conf_static(app:FastAPI):
    app.mount("/static",StaticFiles(directory="backend/static"),name="static")

def create_tables():
    Base.metadata.create_all(bind=engine)    

def start_app():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION) 
    include_routers(app)
    conf_static(app)
    create_tables()
    return app



start_app()

'''@app.get("/",response_class=HTMLResponse)
async def index():
    html_content="""
    <html>
        <head>
            <title>Some Html in here</title>
        </head>
        <body>
            <h1>Look, i made it!!!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content,status_code=status.HTTP_200_OK)'''




