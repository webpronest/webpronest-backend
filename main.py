from fastapi import FastAPI
from app.database import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
# from models.config import active_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Database initialized")

    yield  # <-- app runs here

    # Shutdown: clean up if needed
    print("🛑 Shutting down app")

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)