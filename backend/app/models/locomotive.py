from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base


class Locomotive(Base):
    __tablename__ = "locomotives"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    loco_number = Column(String, unique=True, nullable=False)

    loco_type = Column(String)

    home_shed = Column(String)

    status = Column(String, default="AVAILABLE")