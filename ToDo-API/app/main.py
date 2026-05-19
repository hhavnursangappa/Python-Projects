from fastapi import FastAPI, Depends
from app.database import engine, Base
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine, Base
from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate


# Create database trables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/register")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}
