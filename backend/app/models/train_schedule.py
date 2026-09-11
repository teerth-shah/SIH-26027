from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey

from app.core.database import Base


class TrainSchedule(Base):
    __tablename__ = "train_schedules"

    id = Column(Integer, primary_key=True, index=True)

    train_id = Column(
        Integer,
        ForeignKey("trains.id"),
        nullable=False
    )

    service_date = Column(Date, nullable=False)

    scheduled_departure = Column(DateTime)

    scheduled_arrival = Column(DateTime)

    actual_departure = Column(DateTime)

    actual_arrival = Column(DateTime)

    status = Column(String, default="SCHEDULED")

    delay_minutes = Column(Integer, default=0)