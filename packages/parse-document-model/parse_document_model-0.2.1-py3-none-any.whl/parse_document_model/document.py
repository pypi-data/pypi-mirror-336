import warnings
from abc import ABC
from typing import List, Optional, Union

from pydantic import BaseModel, Field, model_validator

from parse_document_model.attributes import Attributes, PageAttributes, TextAttributes, DocumentAttributes
from parse_document_model.marks import Mark, TextStyleMark, UrlMark


class Node(BaseModel, ABC):
    """Base element of a document.

    A document is a hierarchy of nodes.
    Nodes could represent: document, pages, headings, etc.
    """
    category: str = Field(
        ...,
        title="Node Type",
        description="The type of node. Examples are: `doc`, `page`, `heading`, `body`, etc. For an exhaustive list "
                    "refers to the documentation.",
    )
    attributes: Optional[Attributes] = Field(
        default=None,
        title="Node Attributes",
        description="Attributes related to the node. An example is the reference page."
    )


class StructuredNode(Node):
    content: List[Node] = Field(
        ...,
        title="Node Content",
        description="The content of the node. If it is a leaf node this is text, otherwise it could be a list of "
                    "nodes.",
    )


class Text(Node):
    """The leaf node of a document.

    That's where the actual text is.

    """
    attributes: Optional[TextAttributes] = TextAttributes()
    content: str = Field(
        ...,
        title="Content",
        description="The new field to hold the text content."
    )
    marks: list[Union[Mark, TextStyleMark, UrlMark]] = []
    text: Optional[str] = Field(
        None,
        title="Text",
        description="(Deprecated) This field is deprecated and will be removed in a future version. "
                    "Use `content` instead."
    )
    role: Optional[str] = Field(
        None,
        title="Node Type",
        description="(Deprecated) This field is deprecated and will be removed in a future version. "
                    "Use `category` instead."
    )

    @model_validator(mode="before")
    def handle_deprecations(self):
        if "text" in self and "content" not in self:
            warnings.warn("The use of `text` is deprecated and will be removed in a future version. "
                          "Use `content` instead.", DeprecationWarning)
            self["content"] = self["text"]
        if "role" in self and "category" not in self:
            warnings.warn("The use of `role` is deprecated and will be removed in a future version. "
                          "Use `category` instead.", DeprecationWarning)
            self["category"] = self["role"]
        return self


class Page(StructuredNode):
    """The node that represents a document's page."""
    category: str = "page"
    attributes: Optional[PageAttributes] = None
    content: list[Text]


class Document(StructuredNode):
    """The root node of a document."""
    category: str = "doc"
    attributes: Optional[DocumentAttributes] = None
    content: list[Page]
