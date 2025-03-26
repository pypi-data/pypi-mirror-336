from abc import ABC
from typing import Optional

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    page: int


class Attributes(BaseModel, ABC):
    pass


class DocumentAttributes(Attributes):
    pass


class PageAttributes(Attributes):
    page: int


class TextAttributes(Attributes):
    bounding_box: list[BoundingBox] = []
    level: Optional[int] = Field(None, ge=1, le=4)
    section: Optional[str] = None
