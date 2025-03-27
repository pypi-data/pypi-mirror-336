import typing
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID

from istari_digital_client.configuration import Configuration
from istari_digital_client.openapi_client import ApiClient, NewFunctionAuthSecret
from istari_digital_client.openapi_client import (
    FunctionAuthSecretApi as OpenApiFunctionAuthSecretApi,
)
from istari_digital_client.openapi_client.models.function_auth_type import (
    FunctionAuthType,
)

if typing.TYPE_CHECKING:
    from istari_digital_client import Client

from istari_digital_client.models import (
    FunctionAuthSecret,
    PathLike,
)


class FunctionAuthSecretApi:
    def __init__(
        self,
        config: Configuration,
        client: "Client",
    ) -> None:
        api_client = ApiClient(config.openapi_client_configuration)
        self.openapi_function_auth_secret_api = OpenApiFunctionAuthSecretApi(api_client)
        self.client = client

    def add_function_auth_secret(
        self,
        auth_provider_name: str,
        function_auth_type: FunctionAuthType,
        path: PathLike,
        expiration: Optional[datetime] = None,
    ) -> FunctionAuthSecret:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)

        file_revision = self.client.storage.create_revision(
            file_path=path,
        )

        secret = NewFunctionAuthSecret(
            auth_provider_name=auth_provider_name,
            revision=file_revision,
            function_auth_type=function_auth_type,
            expiration=expiration,
        )

        # noinspection PyArgumentList
        openapi_auth_secret = (
            self.openapi_function_auth_secret_api.add_function_auth_secret(secret)
        )
        return FunctionAuthSecret(openapi_auth_secret, self.client)

    def find_function_auth_secrets(
        self,
        auth_provider_name: Optional[str] = None,
        auth_type: Optional[FunctionAuthType] = None,
        expiration: Optional[datetime] = None,
        latest: Optional[bool] = None,
    ) -> list[FunctionAuthSecret]:
        openapi_secrets = (
            self.openapi_function_auth_secret_api.find_function_auth_secret(
                auth_provider_name, auth_type, expiration, latest
            )
        )
        return [FunctionAuthSecret(s, self.client) for s in openapi_secrets]

    def fetch_function_auth_secret(self, auth_secret_id: UUID) -> FunctionAuthSecret:
        secret = self.openapi_function_auth_secret_api.fetch_function_auth_secret(
            str(auth_secret_id)
        )
        return FunctionAuthSecret(secret, self.client)
