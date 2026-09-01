from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.core.database import Base


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)

    maintenance_task_id = Column(
        Integer,
        ForeignKey("maintenance_task.id"),
        nullable=False
    )

    section_id = Column(
        Integer,
        ForeignKey("sections.id"),
        nullable=False
    )

    planned_start = Column(DateTime, nullable=False)

    planned_end = Column(DateTime, nullable=False)

    actual_start = Column(DateTime)

    actual_end = Column(DateTime)

    status = Column(
        String,
        default="PLANNED"
    )

    priority = Column(Integer, default=1)

    reason = Column(String)