import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Numeric, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_user = Column(UUID(as_uuid=True), nullable=False)
    to_user = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(8), default="USD")
    status = Column(String(16), default="PENDING")
    ts_epoch = Column(DateTime, server_default=text("now()"))
