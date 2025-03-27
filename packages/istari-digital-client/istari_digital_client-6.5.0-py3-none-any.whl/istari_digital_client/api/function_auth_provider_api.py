import typing
from uuid import UUID

from istari_digital_client.configuration import Configuration
from istari_digital_client.openapi_client import ApiClient
from istari_digital_client.openapi_client import (
    FunctionAuthProviderApi as OpenApiFunctionAuthProviderApi,
)
from istari_digital_client.openapi_client.models.function_auth_provider_update import (
    FunctionAuthProviderUpdate,
)

if typing.TYPE_CHECKING:
    from istari_digital_client import Client

from istari_digital_client.models import (
    FunctionAuthProvider,
    FunctionAuthProviderPage,
)


class FunctionAuthProviderApi:
    def __init__(
        self,
        config: Configuration,
        client: "Client",
    ) -> None:
        api_client = ApiClient(config.openapi_client_configuration)
        self.openapi_function_auth_provider_api = OpenApiFunctionAuthProviderApi(
            api_client
        )
        self.client = client

    def add_function_auth_provider(
        self, auth_provider_name: str
    ) -> FunctionAuthProvider:
        auth_provider = (
            self.openapi_function_auth_provider_api.create_function_auth_provider(
                auth_provider_name
            )
        )
        return FunctionAuthProvider(auth_provider, self.client)

    def update_function_auth_provider(
        self, auth_provider_name: str, registration_secret_id: UUID
    ) -> FunctionAuthProvider:
        update = FunctionAuthProviderUpdate(
            registration_secret_id=str(registration_secret_id)
        )
        auth_provider = (
            self.openapi_function_auth_provider_api.update_function_auth_provider(
                auth_provider_name, update
            )
        )
        return FunctionAuthProvider(auth_provider, self.client)

    def list_function_auth_providers(
        self, page: int | None = None, size: int | None = None
    ) -> FunctionAuthProviderPage:
        provider_page = (
            self.openapi_function_auth_provider_api.list_function_auth_provider(
                page, size
            )
        )
        return FunctionAuthProviderPage(provider_page, self.client)
