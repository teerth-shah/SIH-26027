from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.core.database import Base


class Conflict(Base):
    __tablename__ = "conflicts"

    id = Column(Integer, primary_key=True, index=True)

    block_1_id = Column(
        Integer,
        ForeignKey("blocks.id"),
        nullable=False
    )

    block_2_id = Column(
        Integer,
        ForeignKey("blocks.id"),
        nullable=False
    )

    conflict_type = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        default="MEDIUM"
    )

    detected_at = Column(
        DateTime
    )

    resolved = Column(
        Boolean,
        default=False
    )

    resolution = Column(String)