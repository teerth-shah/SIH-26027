from sqlalchemy import Column, Integer, String, DateTime, Float

from app.core.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)

    resource_code = Column(
        String,
        unique=True,
        nullable=False
    )

    resource_type = Column(
        String,
        nullable=False
    )

    name = Column(String)

    status = Column(
        String,
        default="AVAILABLE"
    )

    location = Column(String)

    availability_start = Column(DateTime)

    availability_end = Column(DateTime)

    capacity = Column(Integer, default=1)

    cost_per_hour = Column(Float, default=0)