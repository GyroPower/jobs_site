from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.repository.users import create_new_user
from backend.schemas.User import User_Create
from backend.webapss.users.forms import User_create_form


templates = Jinja2Templates(directory="backend/templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
async def register(request: Request):
    return templates.TemplateResponse(
        name="users/register.html", context={"request": request}
    )


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = User_create_form(request)

    await form.load_data()

    if await form.is_valid():
        user = User_Create(
            username=form.username, email=form.email, password=form.password
        )

        try:
            user = create_new_user(new_user=user, db=db)

            return responses.RedirectResponse(
                "/?msg=Successfully-Registered",
                status_code=status.HTTP_302_FOUND,
            )
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)

    return templates.TemplateResponse("users/register.html", form.__dict__)
