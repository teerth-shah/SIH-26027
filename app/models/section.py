from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.core.database import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)

    section_code = Column(String, unique=True, nullable=False)
    name = Column(String)

    from_station_id = Column(
        Integer,
        ForeignKey("stations.id"),
        nullable=False
    )

    to_station_id = Column(
        Integer,
        ForeignKey("stations.id"),
        nullable=False
    )

    distance_km = Column(Float)

    number_of_tracks = Column(Integer, default=1)

    electrified = Column(Boolean, default=True)

    maximum_speed = Column(Float)

    capacity = Column(Integer)

    status = Column(String, default="AVAILABLE")

    maintenance_allowed = Column(Boolean, default=True)