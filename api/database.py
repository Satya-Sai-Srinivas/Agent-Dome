from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

# The connection string to your Docker PostgreSQL database
# Format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = "postgresql+asyncpg://admin:supersecretpassword@localhost:5432/threat_logs"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Define the SQL Table Schema
class DBLogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Float)
    ip_address = Column(String, index=True)
    method = Column(String)
    endpoint = Column(String)
    user_agent = Column(String)
    payload = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

async def init_db():
    """Creates the tables in the database if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)