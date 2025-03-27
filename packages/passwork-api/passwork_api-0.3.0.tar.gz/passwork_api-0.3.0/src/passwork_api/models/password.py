import base64
from typing import Any, Optional

from pydantic import BaseModel, Field

from passwork_api.models.path import Path


class NewPassword(BaseModel):
    class Config:
        use_enum_values = True

    vault_id: str = Field(..., alias="vaultId", title="Vault ID", description="ID of the vault")
    name: str = Field(..., title="Name", description="Name of the password")
    login: str = Field("", title="Login", description="Login of the password")
    crypted_password: str = Field(..., alias="cryptedPassword", title="Crypted password", description="Crypted password")
    url: str = Field("", title="URL", description="URL of the password")
    description: str = Field("", title="Description", description="Description of the password")
    folder_id: str = Field(..., alias="folderId", title="Folder ID", description="ID of the folder")
    color: Optional[int] = Field(None, title="Color", description="Color of the password")
    tags: list[str] = Field(default_factory=list, title="Tags", description="List of tags")
    is_favorite: bool = Field(False, alias="isFavorite", title="Is favorite", description="Is favorite")

    def __init__(self, **data: Any):
        # encode password
        if "password" in data:
            data["cryptedPassword"] = base64.b64encode(data["password"].encode('utf-8')).decode('utf-8')
            del data["password"]

        super().__init__(**data)

    @property
    def password(self) -> str:
        """
        Returns decrypted password string

        :return: str
        """

        return base64.b64decode(self.crypted_password).decode('utf-8')

    @password.setter
    def password(self, password: str):
        """
        Set password and update crypted_password

        :param password: str
        :return:
        """

        self.crypted_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')


class ExistingPasswordMin(BaseModel):
    class Config:
        use_enum_values = True

    vault_id: str = Field(..., alias="vaultId", title="Vault ID", description="ID of the vault")
    color: Optional[int] = Field(None, title="Color", description="Color of the password")
    folder_id: str = Field(..., alias="folderId", title="Folder ID", description="ID of the folder")
    id: str = Field(..., title="ID", description="ID of the password")
    login: str = Field(..., title="Login", description="Login of the password")
    name: str = Field(..., title="Name", description="Name of the password")
    tags: Optional[list[str]] = Field(None, title="Tags", description="List of tags")
    url: str = Field(..., title="URL", description="URL of the password")
    description: str = Field(..., title="Description", description="Description of the password")


class ExistingPassword(BaseModel):
    class Config:
        use_enum_values = True

    vault_id: str = Field(..., alias="vaultId", title="Vault ID", description="ID of the vault")
    last_password_update: int = Field(..., alias="lastPasswordUpdate", title="Last password update", description="Last password update")
    id: str = Field(..., title="ID", description="ID of the password")
    name: str = Field(..., title="Name", description="Name of the password")
    login: str = Field(..., title="Login", description="Login of the password")
    crypted_password: str = Field(..., alias="cryptedPassword", title="Crypted password", description="Crypted password")
    url: str = Field(..., title="URL", description="URL of the password")
    description: Optional[str] = Field(None, title="Description", description="Description of the password")
    folder_id: str = Field(..., alias="folderId", title="Folder ID", description="ID of the folder")
    color: Optional[int] = Field(None, title="Color", description="Color of the password")
    tags: Optional[list[str]] = Field(None, title="Tags", description="List of tags")
    updated_at: int = Field(..., alias="updatedAt", title="Updated at", description="Updated at")
    path: list[Path] = Field(..., title="Path", description="List of path elements")
    is_favorite: bool = Field(..., alias="isFavorite", title="Is favorite", description="Is favorite")

    @property
    def password(self) -> str:
        """
        Returns decrypted password string

        :return: str
        """

        return base64.b64decode(self.crypted_password).decode('utf-8')
