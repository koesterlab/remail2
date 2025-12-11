"""Database initialization and session management."""

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

# Get or create the database path
DB_PATH = Path.home() / ".remail" / "database.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Initialize database and create all tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Get a database session."""
    return Session(engine)
