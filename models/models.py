from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime(timezone=True), server_default=func.now())
    value = Column(Float)

