from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import jobs
from backend.db.repository.Jobs import create_new_job
from backend.db.repository.Jobs import get_jobs_list
from backend.db.repository.Jobs import r_delete_job
from backend.db.repository.Jobs import r_update_job
from backend.schemas import Jobs
from backend.schemas import User
from backend.security.oauth2 import login_user
from backend.webapss.jobs.form import job_post_form

router = APIRouter()


templates = Jinja2Templates(directory="backend/templates")


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    jobs = get_jobs_list(db)

    return templates.TemplateResponse(
        "general_pages/home_page.html",
        {"request": request, "jobs": jobs.all(), "msg": msg},
    )


@router.get("/detail/{id}")
async def job_detail(id: int, request: Request, db: Session = Depends(get_db)):
    job = get_jobs_list(db, id)
    return templates.TemplateResponse(
        "jobs/detail.html", {"request": request, "job": job.first()}
    )


@router.get("/create")
def create_job(request: Request):
    return templates.TemplateResponse("jobs/create_job.html", {"request": request})


@router.post("/create")
async def create_job(
    request: Request,
    current_user: User.User_response = Depends(login_user.get_current_user),
    db: Session = Depends(get_db),
):
    form = job_post_form(request)

    await form.load_data()

    if await form.is_valid():
        job = Jobs.job_create(**form.__dict__)

        try:
            job = create_new_job(owner_id=current_user.id, new_job=job, db=db)

            return responses.RedirectResponse(
                f"/detail/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us"
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)


@router.put("/update/{id}")
async def update_job(
    id: int,
    update_post_job: Jobs.job_create,
    current_user: User.User_response = Depends(login_user.get_current_user),
    db: Session = Depends(get_db),
):

    updated_job = r_update_job(
        job_id=id, user_id=current_user.id, job_update=update_post_job, db=db
    )

    if not updated_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {id} not found"
        )

    return {"msg": "success"}


@router.delete("/delete/{id}")
async def delete_job(
    id: int,
    current_user: User.User_response = Depends(login_user.get_current_user),
    db: Session = Depends(get_db),
):
    deleted_job = r_delete_job(job_id=id, user_id=current_user.id, db=db)

    if not deleted_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""Job with id {id} not found or don't belong to user
                            {current_user.username}""",
        )
    return {"msg": "success"}
