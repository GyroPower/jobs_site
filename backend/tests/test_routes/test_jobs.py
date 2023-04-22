import json
from typing import List

from fastapi.testclient import TestClient

from backend.schemas.Jobs import job_show


def test_create_job(authorized_client: TestClient):
    data = {
        "title": "Job1",
        "company": "company1",
        "company_url": "www.doodle.com",
        "location": "localhost",
        "description": "python",
    }

    res = authorized_client.post("/jobs/create", json=data)

    assert res.status_code == 200
    assert res.json().get("title") == data["title"]


def test_get_jobs(client: TestClient, create_jobs: List[job_show]):

    res = client.get("/jobs/")

    def validate_jobs(job):
        return job_show(**job)

    if len(res.json()) > 1:

        job_map = map(validate_jobs, res.json())
        jobs = list(job_map)
        assert res.status_code == 200
        assert jobs[0].title == create_jobs[0].title
        assert len(jobs) == len(create_jobs)


def test_get_one_job(client: TestClient, create_jobs: List[job_show]):
    res = client.get("/jobs/?=1")

    assert res.status_code == 200
    assert res.json()[0]["title"] == create_jobs[0].title


def test_update_job(authorized_client: TestClient, create_jobs: List[job_show]):
    data = {
        "title": "company1",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
    }

    data["title"] = "Other"

    res = authorized_client.put("/jobs/update/1", json=data)

    assert res.status_code == 200
    assert res.json().get("msg") == "success"


def test_delete_job(authorized_client: TestClient, create_jobs: List[job_show]):
    res = authorized_client.delete("/jobs/delete/1")

    assert res.status_code == 200
    assert res.json().get("msg") == "success"
