from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table

from .base import Base

module_activity = Table(
    "module_activity",
    Base.metadata,
    Column("module_id", String, ForeignKey("modules.guid"), primary_key=True),
    Column("activity_id", String, ForeignKey("activities.guid"), primary_key=True),
)
