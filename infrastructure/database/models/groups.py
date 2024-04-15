import datetime
from typing import List

from sqlalchemy import TIMESTAMP, func, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base


class Groups(Base):
    __tablename__ = "groups"
    group_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def __repr__(self) -> str:
        return f"Channel(id={self.group_id!r}, name={self.name!r})"


class GroupSettings(Base):
    __tablename__ = "group_settings"
    group_settings_id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id", ondelete="CASCADE"), unique=True)
    frequency: Mapped[str]
    start_time: Mapped[str]
    end_time: Mapped[str]
    status: Mapped[str]
    # status: text(Enum: "active", "inactive")
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def __repr__(self) -> str:
        return f"GroupSettings(id={self.group_settings_id!r} frequency={self.frequency!r} start_time={self.start_time!r} end_time={self.end_time!r} status={self.status!r})"
