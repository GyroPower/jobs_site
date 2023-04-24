from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.apis.version1.route_auth import login_for_access_token
from backend.db.database import get_db
from backend.webapss.auth.forms import Login_form

templates = Jinja2Templates(directory="backend/templates")

router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse(
        name="auth/login.html", context={"request": request}
    )


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = Login_form(request=request)

    await form.load_data()

    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login successful :)")
            response = templates.TemplateResponse(
                name="auth/login.html", context=form.__dict__
            )
            login_for_access_token(form_data=form, db=db, response=response)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect email or password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)
