from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from .charging_event import ChargingEvent

from . import Base
from datetime import datetime


class EventLog(Base):
    __tablename__ = "event_logs"
    __table_args__ = (
        UniqueConstraint(
            "charging_event_id",
            "client_service_id",
            name="uq_event_log_charging_event_service",
        ),
    )

    id = Column(Integer, primary_key=True)
    charging_event_id = Column(
        Integer, ForeignKey("charging_events.id"), nullable=False
    )
    client_service_id = Column(
        Integer, ForeignKey("client_services.id"), nullable=False
    )
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    charging_event = relationship("ChargingEvent")
    client_service = relationship("ClientService", back_populates="event_logs")
