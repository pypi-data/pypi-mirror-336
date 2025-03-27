import logging
from ipaddress import IPv4Address
from typing import Literal, Union, Optional

import requests

from passwork_api.models.folder import ExistingFolder
from passwork_api.models.password import ExistingPasswordMin, ExistingPassword, NewPassword

logger = logging.getLogger("passwork-api")


class PassworkApi:
    def __init__(self, host: Union[str, IPv4Address], port: int, ssl: bool, ssl_verify: bool, auth_token: str, timeout: int):
        self.host = str(host)
        self.port = port
        self.ssl = ssl
        self.ssl_verify = ssl_verify
        self.auth_token = auth_token
        self.timeout = timeout

        logger.debug(f"Create PassworkApi '{self}'.")

        self.api_url: str = ""

        if self.ssl:
            self.api_url += "https://"
        else:
            self.api_url += "http://"

        self.api_url += f"{self.host}:{self.port}/api/v4"

        self._api_token: Optional[str] = None

    def __repr__(self):
        return f"{self.__class__.__name__}(host={self.host}, port={self.port}, ssl={self.ssl}, ssl_verify={self.ssl_verify}, auth_token={self.auth_token})"

    def __str__(self):
        return f"{self.__class__.__name__}(host={self.host}, port={self.port})"

    def __del__(self):
        if self.is_authenticated:
            self.logout()

    def __enter__(self) -> "PassworkApi":
        # login to Passwork API
        _ = self.api_token

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # logout from Passwork API
        if self.is_authenticated:
            self.logout()

    @property
    def api_token(self) -> str:
        if self._api_token is None:
            logger.debug(f"Get API token from {self}.")

            self._api_token = self.auth()

        return self._api_token

    @property
    def is_authenticated(self) -> bool:
        return self._api_token is not None

    def _request(self, method: Literal["GET", "POST", "PUT", "DELETE"], api_path: str, error_message: str, auth: bool = True, **kwargs) -> dict:
        full_url = f"{self.api_url}{api_path}"

        retry = False
        while True:
            logger.debug(f"Request{'(retry)' if retry else ''} '{method}' '{full_url}'.")

            headers = {}

            if auth:
                headers["Passwork-Auth"] = self.api_token

            if "headers" in kwargs:
                headers.update(kwargs["headers"])
                del kwargs["headers"]

            response = requests.request(method, full_url, headers=headers, verify=self.ssl_verify,
                                        timeout=self.timeout, **kwargs)

            if not response.ok:
                if response.status_code == 401 and not retry:
                    logger.debug(f"Request '{method}' '{full_url}' failed with status code {response.status_code}. --> Retry with new API token.")
                    self._api_token = None
                    retry = True
                    continue
                raise requests.exceptions.RequestException(f"{error_message} -> {response.status_code} {response.reason}")
            break

        # try to get json from response
        json = response.json()

        # check if json status 'success'
        if json["status"] != "success":
            raise requests.exceptions.RequestException(f"{error_message} -> {json['status']} {json['message']}")

        return json

    # --- auth section -------------------------------------------------------------------------------------------------------------------------------------------------------------

    def auth(self) -> dict:
        logger.debug(f"Auth to {self}.")
        error_message = f"Could not auth to {self}."

        if self.is_authenticated:
            raise RuntimeError(f"{error_message} -> Already authenticated.")

        json = self._request("POST", f"/auth/login/{self.auth_token}", error_message, auth=False)

        # get token
        if "token" not in json["data"]:
            raise requests.exceptions.RequestException(f"{error_message} -> No token in response data.")
        token = json["data"]["token"]

        logger.debug(f"Auth to {self} successful. -> token={token}")

        return token

    def logout(self):
        logger.debug(f"Logout from {self}.")
        error_message = f"Could not logout from {self}."

        if not self.is_authenticated:
            raise RuntimeError(f"{error_message} -> Not authenticated.")

        self._request("POST", "/auth/logout", error_message)

        self._api_token = None

        logger.debug(f"Logout from {self} successful.")

    # --- folder section -----------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_folder(self, folder_id: str) -> ExistingFolder:
        logger.debug(f"Get folder passwords from {self}.")
        error_message = f"Could not get folder '{folder_id}' from {self}."

        json = self._request("GET", f"/folders/{folder_id}", error_message)

        data = json["data"]

        # validate json data
        folder = ExistingFolder(**data)

        return folder

    def get_folder_passwords(self, folder_id: str) -> list[ExistingPasswordMin]:
        logger.debug(f"Get folder passwords from {self}.")
        error_message = f"Could not get folder '{folder_id}' passwords from {self}."

        json = self._request("GET", f"/folders/{folder_id}/passwords", error_message)

        data = json["data"]

        # validate json data
        passwords = [ExistingPasswordMin(**password) for password in data]

        logger.debug(f"Get folder passwords from {self} successful.")

        return passwords

    # --- password section ---------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_password(self, password_id: str) -> ExistingPassword:
        logger.debug(f"Get password '{password_id}' from {self}.")
        error_message = f"Could not get password '{password_id}' from {self}."

        json = self._request("GET", f"/passwords/{password_id}", error_message)

        data = json["data"]

        # validate json data
        password = ExistingPassword(**data)

        logger.debug(f"Get password '{password_id}' from {self} successful.")

        return password

    def delete_password(self, password_id: str):
        logger.debug(f"Delete password '{password_id}' from {self}.")
        error_message = f"Could not delete password '{password_id}' from {self}."

        self._request("DELETE", f"/passwords/{password_id}", error_message)

        logger.debug(f"Delete password '{password_id}' from {self} successful.")

    def add_password(self, new_password: NewPassword) -> ExistingPassword:
        logger.debug(f"Add password '{new_password.name}' to {self}.")
        error_message = f"Could not add password '{new_password.name}' to {self}."

        json = self._request("POST", "/passwords", error_message, json=new_password.model_dump(by_alias=True))

        data = json["data"]

        # validate json data
        password = ExistingPassword(**data)

        logger.debug(f"Add password '{new_password.name}' to {self} successful.")

        return password
