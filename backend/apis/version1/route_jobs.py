from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import jobs
from backend.db.repository.Jobs import create_new_job
from backend.db.repository.Jobs import get_jobs_list
from backend.db.repository.Jobs import r_delete_job
from backend.db.repository.Jobs import r_search_jobs
from backend.db.repository.Jobs import r_update_job
from backend.schemas import Jobs
from backend.schemas import User
from backend.security.oauth2 import login_user

router = APIRouter()


@router.post("/create", response_model=Jobs.job_show)
async def create_job(
    job: Jobs.job_create,
    current_user: User.User_response = Depends(login_user.get_current_user),
    db: Session = Depends(get_db),
):
    id = current_user.id
    return create_new_job(id, job, db)


@router.get("/", response_model=List[Jobs.job_show])
async def get_jobs(id: Optional[str | None] = None, db: Session = Depends(get_db)):
    jobs = get_jobs_list(db, id)

    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return jobs


@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    jobs = r_search_jobs(term, db=db)
    job_titles = []
    for job in jobs:
        job_titles.append(job.title)
    return job_titles


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
    return {"detail": "successfully deleted"}
