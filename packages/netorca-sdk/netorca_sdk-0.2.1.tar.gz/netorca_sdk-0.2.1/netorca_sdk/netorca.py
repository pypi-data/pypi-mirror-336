from typing import Any, Callable, Dict, Optional, Union

from requests import RequestException, Response

from netorca_sdk.auth import NetorcaAuth
from netorca_sdk.config import API_VERSION, URL_PREFIX
from netorca_sdk.exceptions import (
    NetorcaAPIError,
    NetorcaAuthenticationError,
    NetorcaException,
    NetorcaGatewayError,
    NetorcaInvalidContextError,
    NetorcaNotFoundError,
    NetorcaServerUnavailableError,
    NetorcaValueError,
)
from netorca_sdk.validations import ContextIn


class Netorca:
    """
    Netorca

    A class to manage API calls to various endpoints in the Netorca API using the provided authentication method.

    Attributes:
    - auth (NetorcaAuth): The authentication object used for making API requests.
    - endpoints (Dict): A dictionary containing the supported API endpoints and their corresponding methods.

    Methods:

    __init__(self, auth: NetorcaAuth)
    Initializes the NetorcaEndpointCaller with the provided authentication object.

    caller(self, endpoint: str, operation: str, id: Union[str, int] = None, filters: Dict = None, data: Dict = None, context: ContextIn = None) -> Dict
    Performs the specified operation on the specified endpoint using the provided arguments.

    _get(self, endpoint: str, id: Union[str, int] = None, filters: Dict = None, context: ContextIn = None) -> Dict
    Performs a GET request on the specified endpoint using the provided arguments.

    _create(self, endpoint: str, data: Dict, context: ContextIn = None) -> Dict
    Performs a CREATE request on the specified endpoint using the provided arguments.

    _update(self, endpoint: str, id: Union[str, int], data: Dict, context: ContextIn = None) -> Dict
    Performs an UPDATE request on the specified endpoint using the provided arguments.

    _delete(self, endpoint: str, id: Union[str, int], context: ContextIn = None) -> Dict
    Performs a DELETE request on the specified endpoint using the provided arguments.

    create_url(self, endpoint: str, context: ContextIn = ContextIn.SERVICEOWNER.value, id: Union[str, int] = None)
    Creates the appropriate URL for the specified endpoint, context, and optional ID.
    """

    def __init__(
        self,
        auth: NetorcaAuth = None,
        fqdn: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        verify: bool = True,
    ):
        """
        Initialize Netorca.

        :param auth: (Optional) An existing authentication instance.
        :param fqdn: (Optional) The base URL of the Netorca API (required if no `auth` is provided).
        :param username: (Optional) Username for authentication.
        :param password: (Optional) Password for authentication.
        :param api_key: (Optional) API key for authentication.
        :param verify: (Optional) ignore SSL verification flag.
        """
        if auth:
            # Maintain backward compatibility: Use provided `auth` instance
            self.auth = auth
        elif fqdn:
            # New way: Create `NetorcaAuth` internally
            self.auth = NetorcaAuth(fqdn=fqdn, username=username, password=password, api_key=api_key, verify=verify)
        else:
            raise NetorcaException("Either `auth` or `fqdn` must be provided!")

        self.endpoints: Dict[str, Any] = {
            "services": {
                "get": self._get,
            },
            "service_items": {
                "get": self._get,
            },
            "service_items_dependant": {
                "get": self._get,
                "url": "service_items/dependant",
            },
            "deployed_items": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
                "delete": self._delete,
            },
            "deployed_items_dependant": {
                "get": self._get,
                "url": "deployed_items/dependant",
            },
            "change_instances": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
            },
            "change_instances_dependant": {
                "get": self._get,
                "url": "change_instances/dependant",
            },
            "change_instances_referenced": {
                "get": self._get,
                "url": "change_instances/referenced",
            },
            "service_configs": {
                "get": self._get,
                "create": self._create,
            },
            "charges": {
                "get": self._get,
                "patch": self._update,
                "update": self._update,
                "prefix": "marketplace",
            },
            "charges_accumulated": {
                "get": self._get,
                "url": "charges/accumulated",
                "prefix": "marketplace",
            },
        }

    def caller(
        self,
        endpoint: str,
        operation: str,
        id: Union[str, int] = None,
        filters: Dict = None,
        data: Optional[Dict[str, Any]] = None,
        context: Optional[ContextIn] = None,
    ) -> Dict:
        if endpoint not in self.endpoints:
            raise NetorcaValueError(f"Invalid endpoint: {endpoint}")

        if operation not in self.endpoints[endpoint]:
            raise NetorcaValueError(f"Invalid operation: {operation}")

        if operation == "create":
            return self.endpoints[endpoint][operation](endpoint, data=data, context=context)
        elif operation in {"update", "patch"}:
            return self.endpoints[endpoint][operation](endpoint, id=id, data=data, context=context)
        elif operation == "delete":
            return self.endpoints[endpoint][operation](endpoint, id=id, context=context)
        else:
            return self.endpoints[endpoint][operation](endpoint, id=id, filters=filters, context=context)

    def _get(self, endpoint: str, id: Union[str, int] = None, filters: Dict = None, context: ContextIn = None) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context, id=id)
            response = self.auth.get(url=url, filters=filters)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API GET {e}")

    def _create(self, endpoint: str, data: Dict, context: ContextIn = None) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context)
            response = self.auth.post(url=url, data=data)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API POST {e}")

    def _update(self, endpoint: str, id: Union[str, int], data: Dict, context: ContextIn = None) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context, id=id)
            response = self.auth.patch(url=url, data=data)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API PUT {e}")

    def _delete(self, endpoint: str, id: Union[str, int], context: ContextIn = None) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context, id=id)
            response = self.auth.delete(url=url)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API DELETE {e}")

    def create_url(
        self, endpoint: str, context: Optional[ContextIn] = ContextIn.SERVICEOWNER, id: Union[str, int] = None
    ) -> str:
        id_str = f"{str(id).replace('/', '')}/" if id else ""

        context = ContextIn.SERVICEOWNER if context is None else context
        if context not in (ContextIn.SERVICEOWNER, ContextIn.CONSUMER):
            raise NetorcaInvalidContextError(
                f"{context} is not a valid ContextIn value. Options are {ContextIn.SERVICEOWNER.value} and {ContextIn.CONSUMER.value}"
            )
        endpoints: Dict[str, Any] = self.endpoints if isinstance(self.endpoints, dict) else {}
        custom_url: str = endpoints.get(endpoint, {}).get("url", "")
        url_prefix: str = endpoints.get(endpoint, {}).get("prefix", URL_PREFIX)
        if custom_url:
            url = f"{self.auth.fqdn}/{url_prefix}/{context.value}/{custom_url}/{id_str}"
        else:
            url = f"{self.auth.fqdn}/{url_prefix}/{context.value}/{endpoint}/{id_str}"

        return url

    @staticmethod
    def check_status(response: Response, endpoint: str) -> Dict[Any, Any]:
        """
        Checks the HTTP response status code and raises appropriate exceptions.

        :param response: The HTTP response object.
        :param endpoint: The API endpoint for error context.
        :return: Parsed JSON response if the request was successful.
        :raises: Various exceptions based on the status code.
        """
        status_code = response.status_code

        if status_code in {200, 201}:
            return response.json()
        elif status_code == 204:
            return {"status": "deleted"}
        elif status_code == 400:
            raise NetorcaAPIError(f"Bad request for {endpoint}. Reason: {response.text}")
        elif status_code == 403:
            raise NetorcaAPIError(f"Access denied for {endpoint}.")
        elif status_code == 404:
            raise NetorcaNotFoundError(f"{endpoint} not found.")
        elif status_code == 401:
            raise NetorcaAuthenticationError("Authentication failed.")
        elif status_code == 502:
            raise NetorcaGatewayError("Load balancer or webserver is down.")
        elif status_code == 503:
            raise NetorcaServerUnavailableError("Server is temporarily unavailable.")
        else:
            raise NetorcaAPIError(f"Unexpected error {status_code} for {endpoint}.")
        return {}

    def _validate_context(self, ctx: Union[str, ContextIn, None]) -> ContextIn:
        if ctx is None:
            return ContextIn.SERVICEOWNER
        if isinstance(ctx, ContextIn):
            return ctx
        if isinstance(ctx, str):
            try:
                return ContextIn(ctx.lower())
            except ValueError:
                raise NetorcaInvalidContextError(f"Invalid context '{ctx}'. Must be 'serviceowner' or 'consumer'.")

        raise NetorcaInvalidContextError(f"Invalid type for context: {type(ctx)}. Must be str or ContextIn.")

    def create_deployed_item(self, change_instance_id: int, description: dict) -> dict:
        data = {"deployed_item": description}
        return self.caller("change_instances", "patch", id=change_instance_id, data=data)

    def get_deployed_item(self, change_instance_id: int) -> dict:
        return self.caller("deployed_items", "get", id=change_instance_id)

    def get_deployed_items(self, filters: dict = None, context: Union[str, ContextIn, None] = None) -> dict:
        context_enum = self._validate_context(context)
        return self.caller("deployed_items", "get", context=context_enum, filters=filters)

    def get_service_items(self, filters: dict = None, context: Union[str, ContextIn, None] = None) -> dict:
        context_enum = self._validate_context(context)
        return self.caller("service_items", "get", context=context_enum, filters=filters)

    def get_services(self, filters: dict = None) -> dict:
        return self.caller("services", "get", filters=filters)

    def get_service_item(self, service_item_id: int) -> dict:
        return self.caller("service_items", "get", id=service_item_id)

    def get_change_instance(self, change_instance_id: int) -> dict:
        return self.caller("change_instances", "get", id=change_instance_id)

    def get_change_instances(self, filters: dict = None, context: Union[str, ContextIn, None] = None) -> dict:
        context_enum = self._validate_context(context)
        return self.caller("change_instances", "get", context=context_enum, filters=filters)

    def update_change_instance(self, change_instance_id: int, data: dict) -> dict:
        return self.caller("change_instances", "update", id=change_instance_id, data=data)

    def get_service_config(self, service_config_id: int) -> dict:
        return self.caller("service_configs", "get", id=service_config_id)

    def get_service_configs(self, filters: dict = None) -> dict:
        return self.caller("service_configs", "get", filters=filters)

    def create_service_config(self, data: dict) -> dict:
        return self.caller("service_configs", "create", data=data)

    def get_service_items_dependant(self, filters: dict = None) -> dict:
        return self.caller("service_items_dependant", "get", filters=filters)

    def get_charges(self, filters: dict = None) -> dict:
        return self.caller("charges", "get", filters=filters)

    def update_charges(self, charge_id: int, data: dict) -> dict:
        return self.caller("charges", "patch", id=charge_id, data=data)

    def get_deployed_items_dependant(self, filters: dict = None) -> dict:
        return self.caller("deployed_items_dependant", "get", filters=filters)
