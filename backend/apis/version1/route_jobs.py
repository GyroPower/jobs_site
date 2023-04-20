from backend.db.models import jobs
from backend.security.oauth2 import login_user
from sqlalchemy.orm import Session
from backend.db.database import get_db
from fastapi import APIRouter,Depends,HTTPException,status
from backend.schemas import User,Jobs 
from backend.db.repository.Jobs import create_new_job,get_jobs_list
from typing import List,Optional

router = APIRouter()

@router.post("/create",response_model=Jobs.job_show)
async def create_job( job:Jobs.job_create,
                     current_user:User.User_response= Depends(login_user.get_current_user),
                     db:Session = Depends(get_db)):
    id = current_user.id
    return create_new_job(id,job,db)
    
    
@router.get("/",response_model=List[Jobs.job_show])
async def get_jobs(id:Optional[str|None]=None,db:Session=Depends(get_db)):
    jobs = get_jobs_list(db,id)
    
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return jobs