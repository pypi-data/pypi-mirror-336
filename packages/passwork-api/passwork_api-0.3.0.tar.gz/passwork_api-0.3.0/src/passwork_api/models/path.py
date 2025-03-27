from enum import Enum

from pydantic import BaseModel, Field


class Path(BaseModel):
    class Config:
        use_enum_values = True

    class Type(str, Enum):
        vault = "vault"
        folder = "folder"
        inbox = "inbox"

    order: int = Field(..., title="Order", description="Order of the path")
    name: str = Field(..., title="Name", description="Name of the path")
    type: Type = Field(..., title="Type", description="Type of the path")
    id: str = Field(..., title="ID", description="ID of the path")
