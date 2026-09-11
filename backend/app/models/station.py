from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String, unique=True, nullable=False)
    station_name = Column(String, nullable=False)

    zone = Column(String)
    division = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)