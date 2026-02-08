"""
Database session management.
Provides engine and session factory for SQLModel.
"""
from sqlmodel import Session, create_engine
from src.core.config import settings

# Create database engine with SQLite compatibility
# SQLite requires check_same_thread=False for FastAPI async operations
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.is_development,  # Log SQL queries in development
    connect_args=connect_args,
)


def get_session():
    """
    FastAPI dependency for database sessions.
    Yields a SQLModel session and ensures it's closed after use.

    Usage:
        @app.get("/users")
        def get_users(session: Session = Depends(get_session)):
            users = session.exec(select(User)).all()
            return users
    """
    with Session(engine) as session:
        yield session
