import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, text, DateTime, TIMESTAMP, func, BIGINT
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from infrastructure.database.models.base import Base
from infrastructure.database.models.groups import Groups


class Template(Base):
    __tablename__ = "templates"
    template_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    text: Mapped[Optional[str]]
    photo: Mapped[Optional[str]]
    caption: Mapped[Optional[str]]
    document: Mapped[Optional[str]]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    # messages: Mapped[List["Message"]] = relationship(
    #     back_populates="template",
    # )

    def __repr__(self) -> str:
        return f"Template(id={self.template_id!r}, name={self.name!r}, text={self.text!r})"


class ScheduledMessage(Base):
    __tablename__ = "scheduled_messages"
    scheduled_message_id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("templates.template_id", ondelete="CASCADE"))
    group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("groups.group_id", ondelete="CASCADE"))
    # send_time: text ("HH:MM"): 24-hour format
    send_time: Mapped[str]
    # frequency: text ("1/24", "3/24", "5/72", ...)
    frequency: Mapped[str]
    # status: text (Enum: "scheduled", "sent", "failed", "paused")
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default="scheduled")
    next_send_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    message_link: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    # message = relationship("Message", back_populates="ScheduledMessage")
    # group: Mapped["Groups"] = relationship(back_populates="scheduled_messages")

    def __repr__(self) -> str:
        return f"ScheduledMessage(id={self.scheduled_message_id!r}, group_id={self.group_id!r}, send_time={self.send_time!r}, frequency={self.frequency!r}, status={self.status!r})"


class MessageDeliveryStatus(Base):
    __tablename__ = "message_delivery_status"
    message_delivery_status_id: Mapped[int] = mapped_column(primary_key=True)
    scheduled_message_id: Mapped[int] = mapped_column(ForeignKey("scheduled_messages.scheduled_message_id"))
    # delivery_status: text (Enum: "delivered", "undelivered", "error")
    delivery_status: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    # scheduled_message: Mapped["ScheduledMessage"] = relationship(back_populates="message_delivery_status")

    def __repr__(self) -> str:
        return f"MessageDeliveryStatus(id={self.message_delivery_status_id!r}, scheduled_message_id={self.scheduled_message_id!r}, delivery_status={self.delivery_status!r})"
