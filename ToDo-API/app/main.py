from fastapi import FastAPI
from app.database import engine, Base
from contextlib import asynccontextmanager


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
