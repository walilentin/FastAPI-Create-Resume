from io import BytesIO

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, desc, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse, HTMLResponse

from src.chat.router import router as router_chat
from src.database import get_async_session
from src.resume.models import Resume
from src.resume.schemas import ResumeCreate
from src.users.base_config import fastapi_users, auth_backend
from src.users.manager import get_user_manager
from src.users.schemas import UserCreate, UserRead
from src.resume.router import router as resume_router
from fastapi.responses import RedirectResponse
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/login")
def get_chat_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/secured")
async def secured_route(current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
    if current_user:
        return {"message": "Секретна сторінка", "user": current_user}
    return {"message": "Секретна сторінка без авторизації"}

@app.get("/")
async def home(request: Request, session: AsyncSession = Depends(get_async_session), current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
    if current_user:
        query = select(Resume).where(Resume.user_id == current_user.id).order_by(desc(Resume.id)).limit(1)
        resume = await session.execute(query)
        resume = resume.scalar_one_or_none()
    else:
        resume = None
    return templates.TemplateResponse("base.html", {"request": request, "user": current_user, "resume": resume})

@app.get("/chat")
async def get_chat_page(request: Request, current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
    return templates.TemplateResponse("chat.html", {"request": request, "user": current_user})

@app.get("/data_input")
async def data_input(request: Request, current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
    return templates.TemplateResponse("data_input.html", {"request": request, "user": current_user})

@app.get("/all_resumes")
async def get_all_resumes(request: Request, current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)), session: AsyncSession = Depends(get_async_session)):
    if current_user:
        query = select(Resume).where(Resume.user_id == current_user.id)
        resume = await session.execute(query)
        resume = resume.scalars().all()
    else:
        resume = None
    return templates.TemplateResponse("all_resumes.html", {"request": request, "user": current_user, "resume": resume})


    return StreamingResponse(BytesIO(resume.photo), media_type="image/jpeg")
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/register",
    tags=["register"],
)
app.include_router(router_chat)
app.include_router(resume_router)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
