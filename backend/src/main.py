"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from src.core.config import settings
from src.db.session import engine

# Import models to register them with SQLModel metadata
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)


@app.on_event("startup")
def on_startup():
    """
    Create database tables on application startup.
    This ensures all tables exist before handling requests.
    """
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    """
    Root endpoint - API health check.
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring and deployment.
    """
    return {"status": "healthy"}


# Import and include routers
from src.api import auth
from src.api.routes import tasks, chat

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router)
app.include_router(chat.router)
