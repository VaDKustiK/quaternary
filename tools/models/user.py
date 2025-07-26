from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from tools.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    name_en = Column(String)
    surname_en = Column(String)

    orcid = Column(String)
    internet_profile = Column(String)
    degrees = Column(String)
    degrees_en = Column(String)
    occupation = Column(String)
    occupation_en = Column(String)
    position = Column(String)
    position_en = Column(String)
    interests = Column(String)
    interests_en = Column(String)
    city = Column(String)
    city_en = Column(String)
    address = Column(String)
    address_en = Column(String)
    country = Column(String)
    state = Column(String)

    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_admin = Column(Boolean, default=False)