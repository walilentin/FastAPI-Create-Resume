from sqlalchemy import Column, Integer, String, MetaData,ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base

metadata = MetaData()

class Resume(Base):
    __tablename__ = "resume"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Внешний ключ на пользователя
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    birthdate = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String, nullable=False)
    github = Column(String, nullable=False)
    education = Column(String)
    additional_education = Column(String)
    skills = Column(String, nullable=False)
    projects = Column(String)
    photo = Column(String, nullable=True)
    user = relationship("User", back_populates="resumes")  # Обратная связь с пользователем