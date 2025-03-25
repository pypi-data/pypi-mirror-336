from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from .base import Base
from .joins import module_activity
from .textbook import Textbook

if TYPE_CHECKING:
    from .module import Module


class Activity(MappedAsDataclass, Base):
    __tablename__ = "activities"

    guid: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, insert_default=uuid.uuid4
    )

    name: Mapped[str]
    description: Mapped[str]
    prompt: Mapped[str]

    textbook_guid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("textbooks.guid"),
        init=False,
    )
    textbook: Mapped[Textbook] = relationship(back_populates="activities", init=False)

    modules: Mapped[set[Module]] = relationship(
        default_factory=set,
        back_populates="activities",
        secondary=module_activity,
    )

    def __hash__(self) -> int:
        return hash(self.guid)
