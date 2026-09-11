from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.core.database import Base


class ResourceAssignment(Base):
    __tablename__ = "resource_assignments"

    id = Column(Integer, primary_key=True, index=True)

    maintenance_task_id = Column(
        Integer,
        ForeignKey("maintenance_task.id"),
        nullable=False
    )

    resource_id = Column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False
    )

    assigned_from = Column(DateTime)

    assigned_until = Column(DateTime)

    status = Column(
        String,
        default="ASSIGNED"
    )