import uuid
from sqlalchemy import Column, String, Boolean, Date, ForeignKey, Float, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
metadata = MetaData()
class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    salaries = relationship("Salary", back_populates="user")

class Salary(Base):
    __tablename__ = "salaries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    user = relationship("User", back_populates="salaries")
    amount = Column(Float, nullable=False)
    next_raise_date = Column(Date, nullable=True)
