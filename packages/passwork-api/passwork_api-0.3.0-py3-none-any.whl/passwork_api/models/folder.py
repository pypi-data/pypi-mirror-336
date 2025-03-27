from pydantic import BaseModel, Field

from passwork_api.models.path import Path


class ExistingFolder(BaseModel):
    class Config:
        use_enum_values = True

    vault_id: str = Field(..., alias="vaultId", title="Vault ID", description="ID of the vault")
    name: str = Field(..., title="Name", description="Name of the folder")
    id: str = Field(..., title="ID", description="ID of the folder")
    parent_id: str = Field(..., alias="parentId", title="Parent ID", description="ID of the parent folder")
    path: list[Path] = Field(..., title="Path", description="List of path elements")
