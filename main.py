from fastapi import FastAPI, Depends, Request
from app.database import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from models.config import *
from routers.auth import verify_jwt, router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_session as get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("✅ Database initialized")

    yield  # <-- app runs here

    # Shutdown: clean up if needed
    print("🛑 Shutting down app")

PUBLIC_PATHS = [
    "/docs",
    "/openapi.json",
    "/redoc",
    "/health",
    "/auth/google/callback",
    "/auth/logout",
]

async def protected_routes_dependency(request: Request = None, db=Depends(get_db)):
    if request.url.path not in PUBLIC_PATHS:
        print("🔒 Protected route:", request.url.path)
        return await verify_jwt(request, db)
    else:
        print("🔓 Public route:", request.url.path)
        return None


# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan, dependencies=[Depends(protected_routes_dependency)])

origins = [
    "http://localhost:3000",
    "https://webpronest.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)

@app.get("/me")
async def read_me(request: Request):
    user = request.state.user
    return user

@app.get("/health")
async def health_check():
    return {"status": "ok"}