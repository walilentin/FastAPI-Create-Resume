
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.resume.models import Resume
from src.resume.schemas import ResumeCreate
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@router.post("")
async def res(new_resume: ResumeCreate, session: AsyncSession = Depends(get_async_session), current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
    stmt = insert(Resume).values(user_id=current_user.id, **new_resume.dict())  # Связываем резюме с текущим пользователем
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

