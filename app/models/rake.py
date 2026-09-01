from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base


class Rake(Base):
    __tablename__ = "rakes"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    rake_number = Column(String, unique=True, nullable=False)

    rake_type = Column(String)

    coach_count = Column(Integer)

    capacity = Column(Integer)

    home_depot = Column(String)

    status = Column(String, default="AVAILABLE")