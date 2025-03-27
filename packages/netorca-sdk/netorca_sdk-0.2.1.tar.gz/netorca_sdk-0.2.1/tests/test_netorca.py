from typing import Any, Dict
from unittest.mock import MagicMock, create_autospec, patch

import pytest

from netorca_sdk.auth import NetorcaAuth
from netorca_sdk.exceptions import NetorcaAPIError, NetorcaInvalidContextError, NetorcaNotFoundError, NetorcaValueError
from netorca_sdk.netorca import Netorca
from netorca_sdk.validations import ContextIn, InvalidContextError


@pytest.fixture
def auth_mock() -> MagicMock:
    """
    Fixture to create a MagicMock of the NetorcaAuth class.
    """
    auth: MagicMock = MagicMock(spec=NetorcaAuth)
    auth.fqdn = "https://api.example.com"
    return auth


@pytest.fixture
def endpoint_caller(auth_mock: MagicMock) -> Netorca:
    """
    Fixture to create an instance of Netorca with a MagicMock of the NetorcaAuth class.
    """
    return Netorca(auth_mock)


@pytest.mark.parametrize(
    "status_code, result, error_message", [(200, {"result": "success"}, None), (404, None, "deployed_items not found")]
)
def test_get(
    status_code: int, result: Dict[Any, Any], error_message: str, auth_mock: MagicMock, endpoint_caller: Netorca
) -> None:
    """
    Test the 'get' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result if result else {"error": "not found"}

    if error_message:
        with pytest.raises(NetorcaNotFoundError, match=error_message):
            endpoint_caller.caller("deployed_items", "get", id=1)
    else:
        res = endpoint_caller.caller("deployed_items", "get", id=1)
        auth_mock.get.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message",
    [(201, {"result": "created"}, None), (400, None, "Error 400 - could not create data")],
)
def test_create(
    status_code: int, result: Dict[Any, Any], error_message: str, auth_mock: MagicMock, endpoint_caller: Netorca
) -> None:
    """
    Test the 'post' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.post.return_value.status_code = status_code
    auth_mock.post.return_value.json.return_value = result if result else "could not create data"

    data = {"field": "value"}
    if error_message:
        with pytest.raises(NetorcaAPIError):
            endpoint_caller.caller("deployed_items", "create", data=data)
    else:
        res = endpoint_caller.caller("deployed_items", "create", data=data)
        auth_mock.post.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(200, {"result": "updated"}, None), (400, None, "Could not update data")]
)
def test_update(
    status_code: int, result: Dict[Any, Any], error_message: str, auth_mock: MagicMock, endpoint_caller: Netorca
) -> None:
    """
    Test the 'update' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.patch.return_value.status_code = status_code
    auth_mock.patch.return_value.json.return_value = (
        result if result else {"error": "Error - 400 - Could not update data"}
    )

    data = {"field": "new_value"}
    if error_message:
        with pytest.raises(NetorcaAPIError):
            endpoint_caller.caller("deployed_items", "update", id=1, data=data)
    else:
        res = endpoint_caller.caller("deployed_items", "update", id=1, data=data)
        auth_mock.patch.assert_called_once()
        assert res == result


@pytest.mark.parametrize(
    "status_code, result, error_message", [(204, {"status": "deleted"}, None), (404, None, "deployed_items not found")]
)
def test_delete(
    status_code: int, result: Dict[Any, Any], error_message: str, auth_mock: MagicMock, endpoint_caller: Netorca
) -> None:
    """
    Test the 'delete' operation of the Netorca 'caller' method with various response status codes.
    """
    auth_mock.delete.return_value.status_code = status_code
    auth_mock.delete.return_value.json.return_value = {"error": "not found"} if status_code == 404 else None

    if error_message:
        with pytest.raises(NetorcaNotFoundError, match=error_message):
            endpoint_caller.caller("deployed_items", "delete", id=1)
    else:
        res = endpoint_caller.caller("deployed_items", "delete", id=1)
        assert res == result


def test_invalid_endpoint_or_operation(auth_mock: MagicMock, endpoint_caller: Netorca) -> None:
    """
    Test function to ensure that an appropriate ValueError is raised when an invalid
    endpoint or operation is specified when calling the 'caller' method of the 'Netorca'
    class instance.
    """
    with pytest.raises(NetorcaValueError, match="Invalid endpoint"):
        endpoint_caller.caller("nonexistent_endpoint", "delete", id=1)

    with pytest.raises(NetorcaValueError, match="Invalid operation"):
        endpoint_caller.caller("deployed_items", "nonexistent_operation", id=1)


def test_create_url_context_handling(auth_mock: MagicMock, endpoint_caller: Netorca) -> None:
    """
    Test function to ensure that the 'create_url' method of the 'Netorca' class returns the
    correct URL string for various context and ID values.
    """
    endpoint = "deployed_items"
    url_serviceowner = "https://api.example.com/orcabase/serviceowner/deployed_items/"
    url_consumer = "https://api.example.com/orcabase/consumer/deployed_items/"
    wrong_context = MagicMock()
    wrong_context.value = "wrong_context"

    assert endpoint_caller.create_url(endpoint, context=ContextIn.SERVICEOWNER) == url_serviceowner
    assert endpoint_caller.create_url(endpoint, context=ContextIn.CONSUMER) == url_consumer

    # Test with default context value (assuming ContextIn.SERVICEOWNER is the default)
    assert endpoint_caller.create_url(endpoint) == url_serviceowner

    # Test with an invalid context value
    with pytest.raises(NetorcaInvalidContextError):
        endpoint_caller.create_url(endpoint, context=wrong_context)

    # Test with a wrong context type (e.g., a string instead of a ContextIn)
    with pytest.raises(NetorcaInvalidContextError):
        endpoint_caller.create_url(endpoint, context=wrong_context)


def test_get_service_items(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_service_items()` works the same as `netorca.caller("service_items", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_items", "get")
    result_get_service_items = netorca.get_service_items()

    assert result_caller == result_get_service_items


def test_create_deployed_item(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.create_deployed_item()` works the same as `netorca.caller("change_instances", "patch")`.
    """
    change_instance_id = 34
    description = {"field": "value"}

    status_code = 200
    result = {"result": "success"}

    auth_mock.patch.return_value.status_code = status_code
    auth_mock.patch.return_value.json.return_value = result

    result_caller = endpoint_caller.caller(
        "change_instances", "patch", id=change_instance_id, data={"deployed_item": description}
    )
    result_create_deployed_item = netorca.create_deployed_item(change_instance_id, description)

    assert result_caller == result_create_deployed_item


def test_get_deployed_item(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_deployed_item()` works the same as `netorca.caller("deployed_items", "get")`.
    """
    change_instance_id = 34

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("deployed_items", "get", id=change_instance_id)
    result_get_deployed_item = netorca.get_deployed_item(change_instance_id)

    assert result_caller == result_get_deployed_item


def test_get_deployed_items(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_deployed_items()` works the same as `netorca.caller("deployed_items", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("deployed_items", "get")
    result_get_deployed_items = netorca.get_deployed_items()

    assert result_caller == result_get_deployed_items


def test_get_service_item(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_service_item()` works the same as `netorca.caller("service_items", "get")`.
    """
    service_item_id = 333

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_items", "get", id=service_item_id)
    result_get_service_item = netorca.get_service_item(service_item_id)

    assert result_caller == result_get_service_item


def test_get_change_instance(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_change_instance()` works the same as `netorca.caller("change_instances", "get")`.
    """
    change_instance_id = 333

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("change_instances", "get", id=change_instance_id)
    result_get_change_instance = netorca.get_change_instance(change_instance_id)

    assert result_caller == result_get_change_instance


def test_get_change_instances(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_change_instances()` works the same as `netorca.caller("change_instances", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("change_instances", "get")
    result_get_change_instances = netorca.get_change_instances()

    assert result_caller == result_get_change_instances


def test_update_change_instance(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.update_change_instance()` works the same as `netorca.caller("change_instances", "update")`.
    """
    change_instance_id = 43
    data = {"field": "new_value"}

    status_code = 200
    result = {"result": "success"}

    auth_mock.patch.return_value.status_code = status_code
    auth_mock.patch.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("change_instances", "update", id=change_instance_id, data=data)
    result_update_change_instance = netorca.update_change_instance(change_instance_id, data)

    assert result_caller == result_update_change_instance


def test_get_service_config(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_service_config()` works the same as `netorca.caller("service_configs", "get")`.
    """
    service_config_id = 17

    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_configs", "get", id=service_config_id)
    result_get_service_config = netorca.get_service_config(service_config_id)

    assert result_caller == result_get_service_config


def test_get_service_configs(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_service_configs()` works the same as `netorca.caller("service_configs", "get")`.
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_configs", "get")
    result_get_service_configs = netorca.get_service_configs()

    assert result_caller == result_get_service_configs


def test_get_service_items_dependant(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_service_items_dependant()` works the same as `netorca.caller("service_items_dependant", "get")`
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("service_items_dependant", "get")
    result_get_service_items_dependant = netorca.get_service_items_dependant()

    assert result_caller == result_get_service_items_dependant


def test_get_deployed_items_dependant(endpoint_caller: Netorca, auth_mock: MagicMock, netorca: Netorca) -> None:
    """
    Test if `netorca.get_deployed_items_dependant()` works the same as `netorca.caller("deployed_items_dependant", "get")`
    """
    status_code = 200
    result = {"result": "success"}

    auth_mock.get.return_value.status_code = status_code
    auth_mock.get.return_value.json.return_value = result

    result_caller = endpoint_caller.caller("deployed_items_dependant", "get")
    result_get_deployed_items_dependant = netorca.get_deployed_items_dependant()

    assert result_caller == result_get_deployed_items_dependant


@pytest.mark.parametrize(
    "method_name, endpoint",
    [
        ("get_deployed_items", "deployed_items"),
        ("get_change_instances", "change_instances"),
        ("get_service_items", "service_items"),
    ],
)
class TestNetorcaContextCalls:
    @pytest.mark.parametrize(
        "context_input, expected_enum",
        [
            (None, ContextIn.SERVICEOWNER),  # Passing nothing => default SERVICEOWNER
            ("serviceowner", ContextIn.SERVICEOWNER),
            ("consumer", ContextIn.CONSUMER),
        ],
    )
    def test_call_methods_with_valid_context(
        self,
        method_name: str,
        endpoint: str,
        context_input: str,
        expected_enum: ContextIn,
    ) -> None:
        """
        Call each method with different 'context' values and
        confirm the 'create_url' is called with the correct enum.
        We also patch auth.get so it returns a 'status_code' of 200
        to avoid NetorcaAPIError from the MagicMock object.
        """
        netorca = Netorca(auth=MagicMock(fqdn="https://api.example.com"))

        with patch.object(netorca.auth, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"mocked": "data"}
            mock_get.return_value = mock_response

            func = getattr(netorca, method_name)
            result = func(context=context_input)
            called_url = mock_get.call_args[1]["url"]
            base_url = "https://api.example.com/orcabase"
            expected_url = f"{base_url}/{expected_enum.value}/{endpoint}/"
            assert called_url == expected_url, f"URL mismatch: expected {expected_url} got {called_url}"
            assert result == {"mocked": "data"}

    def test_call_methods_with_invalid_context(self, method_name: str, endpoint: str) -> None:
        """
        Passing an invalid string (or invalid enum) for context
        should raise NetorcaInvalidContextError.
        """
        netorca = Netorca(auth=MagicMock(fqdn="https://api.example.com"))

        func = getattr(netorca, method_name)
        with pytest.raises(NetorcaInvalidContextError) as exc:
            func(context="not_real_context")  # invalid

        assert "Invalid context 'not_real_context'. Must be 'serviceowner' or 'consumer'." in str(exc.value)
