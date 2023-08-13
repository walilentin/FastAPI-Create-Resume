
from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from src.database import get_async_session
from src.resume.models import Resume
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager
from src.resume.schemas import ResumeCreate
router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@router.post("")
async def res(new_resume: ResumeCreate,session: AsyncSession = Depends(get_async_session), current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
    stmt = insert(Resume).values(user_id=current_user.id, **new_resume.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}



