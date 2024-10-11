from fastapi import FastAPI
from app.api.routes import auth
from app.db.database import engine
from app.db.models import Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def startup(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

app = FastAPI(lifespan=startup)

app.include_router(auth.router, prefix="/auth")
