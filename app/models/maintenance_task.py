from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.core.database import Base


class MaintenanceTask(Base):
    __tablename__ = "maintenance_task"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    maintenance_type = Column(String, nullable=False)

    description = Column(String)

    priority = Column(Integer, default=1)

    required_duration_minutes = Column(Integer, nullable=False)

    earliest_start = Column(DateTime)

    latest_finish = Column(DateTime)

    deadline = Column(DateTime)

    required_crew_type = Column(String)

    status = Column(String, default="PENDING")

    safety_clearance_required = Column(Boolean, default=False)