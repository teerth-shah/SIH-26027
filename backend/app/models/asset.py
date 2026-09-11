from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    asset_code = Column(String, unique=True, nullable=False)

    asset_type = Column(String, nullable=False)

    name = Column(String)

    location = Column(String)

    status = Column(String, default="AVAILABLE")

    commissioned_date = Column(Date)

    last_maintenance_date = Column(Date)

    next_maintenance_due = Column(Date)