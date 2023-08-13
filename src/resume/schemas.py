from datetime import date

from pydantic import BaseModel, EmailStr

class ResumeCreate(BaseModel):
    full_name: str
    address: str
    birthdate: str
    phone: str
    email: str
    github: str
    education: str = None
    additional_education: str = None
    skills: str
    projects: str = None
