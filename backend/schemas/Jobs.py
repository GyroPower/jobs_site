from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class job_base(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    location: Optional[str] = "Remote"
    description: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()
    owner_id: str


class job_create(BaseModel):

    title: str
    company: str
    location: str
    description: str


class job_show(job_base):
    title: str
    company: str
    company_url: Optional[str]
    location: str
    date_posted: date
    description: Optional[str]
    owner_id = str

    class Config:
        orm_mode = True
