from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .email import Email


class EmailTag(SQLModel, table=True):
    __tablename__ = "email_tags"

    id: int | None = Field(default=None, primary_key=True)
    email_id: int = Field(foreign_key="emails.id", nullable=False)
    tag: str = Field(nullable=False)

    email: "Email" = Relationship(back_populates="tags")