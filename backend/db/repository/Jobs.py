from sqlalchemy.orm import Session
from backend.schemas.Jobs import job_create
from backend.schemas.User import User_response
from backend.db.models import jobs
from typing import Optional

def create_new_job(owner_id:int,new_job:job_create,db:Session):
    job = jobs.Jobs(**new_job.dict(),owner_id=owner_id)
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    return job

def get_jobs_list( db:Session,id:Optional[str|None]=None):
    
    if id is None:
        posts = db.query(jobs.Jobs).filter(jobs.Jobs.is_active==True).all()
    else:
        posts = db.query(jobs.Jobs).filter(jobs.Jobs.is_active==True).filter(jobs.Jobs.id==id).all()
    
    return posts