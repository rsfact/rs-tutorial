from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
from datetime import datetime

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    from_name = Column(String, unique=True, index=True)
    to_url = Column(String)
    count = Column(Integer, default=0)
    created_at = Column(String, default=lambda: datetime.now().isoformat())
    description = Column(String, nullable=True)
