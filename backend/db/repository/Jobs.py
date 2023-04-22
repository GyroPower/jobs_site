from typing import Optional

from sqlalchemy.orm import Session

from ...db.models import jobs
from ...schemas.Jobs import job_create


def create_new_job(owner_id: int, new_job: job_create, db: Session):
    job = jobs.Jobs(**new_job.dict(), owner_id=owner_id)

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_jobs_list(db: Session, id: Optional[str | None] = None):

    if id is None:
        posts = db.query(jobs.Jobs).filter(jobs.Jobs.is_active == True).all()
    else:
        posts = (
            db.query(jobs.Jobs)
            .filter(jobs.Jobs.is_active == True)
            .filter(jobs.Jobs.id == id)
            .all()
        )

    return posts


def r_update_job(job_id: int, user_id: int, job_update: job_create, db: Session):

    job = (
        db.query(jobs.Jobs)
        .filter(jobs.Jobs.id == job_id)
        .filter(jobs.Jobs.owner_id == user_id)
    )

    if not job.first():
        return 0

    job.update(job_update.__dict__)
    db.commit()
    return 1


def r_delete_job(job_id: int, user_id: int, db: Session):
    job = (
        db.query(jobs.Jobs)
        .filter(jobs.Jobs.id == job_id)
        .filter(jobs.Jobs.owner_id == user_id)
    )

    if not job.first():
        return False

    job.delete(synchronize_session=False)
    db.commit()
    return True
