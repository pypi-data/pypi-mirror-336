from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class TemplateVariablesCollection(BaseModel):
    """Collection of template variables."""

    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class CreateCollectionRequest(BaseModel):
    """Request to create a new template variables collection."""

    name: str | None = None
    description: str = ""
