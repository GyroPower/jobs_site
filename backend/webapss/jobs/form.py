from typing import List
from typing import Optional

from fastapi import Request


class job_post_form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.title: Optional[str] = None
        self.company: Optional[str] = None
        self.company_url: Optional[str] = None
        self.location: Optional[str] = "Remote"
        self.description: Optional[str] = None
        self.errors: List = []

    async def load_data(self):
        form = await self.request.form()

        self.title = form.get("title")
        self.company = form.get("company")
        self.company_url = form.get("company_url")
        self.job_location = form.get("location")
        self.description = form.get("description")

    async def is_valid(self):
        if not self.title or not len(self.title) >= 4:
            self.errors.append("A valid title is required")
        if not self.company or not len(self.company) >= 1:
            self.errors.append("A valid company is required")
        if not self.company_url or not self.company_url.__contains__("http"):
            self.errors.append("A valid URL is required e.g. https://example.com")
        if not self.description or not len(self.description) >= 20:
            self.errors.append("Description is too short")

        if not self.errors:
            return True
        return False
