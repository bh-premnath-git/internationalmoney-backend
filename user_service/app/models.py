import uuid
from datetime import datetime

from sqlalchemy import String, text, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    role = Column(String(32), nullable=False, default="user")
    created_at = Column(DateTime, server_default=text("now()"))
