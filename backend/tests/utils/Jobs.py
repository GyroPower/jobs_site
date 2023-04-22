from sqlalchemy.orm import Session

from ...db.models import jobs
from ...schemas.User import User_response


def create_various_jobs(test_user: User_response, db_session: Session):

    data = [
        {
            "title": "company1",
            "company": "doogle",
            "company_url": "www.doogle.com",
            "location": "USA,NY",
            "description": "python",
        },
        {
            "title": "company2",
            "company": "foogle",
            "company_url": "www.foogle.com",
            "location": "USA,LA",
            "description": "python",
        },
        {
            "title": "company3",
            "company": "poogle",
            "company_url": "www.poogle.com",
            "location": "USA,NY",
            "description": "python",
        },
    ]

    def create_jobs_(job):
        return jobs.Jobs(**job, owner_id=test_user["id"])

    jobs_map = map(create_jobs_, data)
    jobs_list = list(jobs_map)
    db_session.add_all(jobs_list)
    db_session.commit()
    return db_session.query(jobs.Jobs).all()
