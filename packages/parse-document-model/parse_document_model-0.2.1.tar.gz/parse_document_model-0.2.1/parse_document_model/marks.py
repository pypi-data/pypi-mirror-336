from typing import Any
from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class Color(BaseModel):
    id: str
    r: int
    g: int
    b: int


class Font(BaseModel):
    id: str
    name: str
    size: int


class Mark(BaseModel):
    category: Literal['bold', 'italic', 'textStyle', 'link']

    @model_validator(mode='before')
    def check_details(self: Any) -> Any:
        mark_type = self.get('category')

        if mark_type == 'textStyle':
            if 'color' not in self and 'font' not in self:
                raise ValueError('color or font must be provided when type is textStyle')
            if 'url' in self:
                raise ValueError('url should not be provided when type is textStyle')

        elif mark_type == 'link':
            if 'url' not in self:
                raise ValueError('url must be provided when type is link')
            if 'textStyle' in self:
                raise ValueError('textStyle should not be provided when type is link')
        return self


class TextStyleMark(Mark):
    color: Optional[Color] = None
    font: Optional[Font] = None


class UrlMark(Mark):
    url: str
