from sqlalchemy import Column, Integer, String, ForeignKey

from app.core.database import Base


class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)

    train_number = Column(String, unique=True, nullable=False)

    train_name = Column(String)

    train_type = Column(String)

    priority = Column(Integer, default=1)

    origin_station_id = Column(
        Integer,
        ForeignKey("stations.id"),
        nullable=False
    )

    destination_station_id = Column(
        Integer,
        ForeignKey("stations.id"),
        nullable=False
    )

    rake_id = Column(
        Integer,
        ForeignKey("rakes.id"),
        nullable=True
    )

    locomotive_id = Column(
        Integer,
        ForeignKey("locomotives.id"),
        nullable=True
    )

    status = Column(String, default="SCHEDULED")

    delay_minutes = Column(Integer, default=0)