from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.update_incident_request import UpdateIncidentRequest
from ...models.update_incident_response import UpdateIncidentResponse


def _get_kwargs(
    incident_id: str,
    *,
    body: UpdateIncidentRequest,
    sysparm_input_display_value: Optional[bool] = None,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["sysparm_input_display_value"] = sysparm_input_display_value

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/incident/{incident_id}".format(
            incident_id=incident_id,
        ),
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, UpdateIncidentResponse]]:
    if response.status_code == 200:
        response_200 = UpdateIncidentResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = DefaultError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = DefaultError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = DefaultError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = DefaultError.from_dict(response.json())

        return response_404
    if response.status_code == 405:
        response_405 = DefaultError.from_dict(response.json())

        return response_405
    if response.status_code == 406:
        response_406 = DefaultError.from_dict(response.json())

        return response_406
    if response.status_code == 409:
        response_409 = DefaultError.from_dict(response.json())

        return response_409
    if response.status_code == 415:
        response_415 = DefaultError.from_dict(response.json())

        return response_415
    if response.status_code == 500:
        response_500 = DefaultError.from_dict(response.json())

        return response_500
    if response.status_code == 402:
        response_402 = DefaultError.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DefaultError, UpdateIncidentResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    incident_id_lookup: Any,
    incident_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateIncidentRequest,
    sysparm_input_display_value: Optional[bool] = None,
) -> Response[Union[DefaultError, UpdateIncidentResponse]]:
    """Update Incident

     Update an incident

    Args:
        incident_id (str): Start typing the incident number to find the incident that needs to be
            updated
        sysparm_input_display_value (Optional[bool]): ServiceNow REST API stores the date-time in
            the UTC time zone unless you specify sysparm_input_display_value to true.

            If you specify sysparm_input_display_value to true, then the date-time is stored exactly
            what you sent in the request.

            If not, the date-time sent via REST API is converted to the UTC time based on the User's
            timezone(User initiating the REST call)

            If the User's time zone is not set then the system time is taken for reference to convert
            to UTC.
        body (UpdateIncidentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateIncidentResponse]]
    """

    if not incident_id and incident_id_lookup:
        filter = incident_id_lookup
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url=f"/incident?where=number like '{filter}'"
        )
        lookup_response = lookup_response_raw.json()

        found_items = lookup_response

        if not found_items:
            raise ValueError("No matches found for incident_id_lookup in incident")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for incident_id_lookup in incident. Using the first match."
            )

        incident_id = found_items[0]["sys_id"]

    kwargs = _get_kwargs(
        incident_id=incident_id,
        body=body,
        sysparm_input_display_value=sysparm_input_display_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    incident_id_lookup: Any,
    incident_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateIncidentRequest,
    sysparm_input_display_value: Optional[bool] = None,
) -> Optional[Union[DefaultError, UpdateIncidentResponse]]:
    """Update Incident

     Update an incident

    Args:
        incident_id (str): Start typing the incident number to find the incident that needs to be
            updated
        sysparm_input_display_value (Optional[bool]): ServiceNow REST API stores the date-time in
            the UTC time zone unless you specify sysparm_input_display_value to true.

            If you specify sysparm_input_display_value to true, then the date-time is stored exactly
            what you sent in the request.

            If not, the date-time sent via REST API is converted to the UTC time based on the User's
            timezone(User initiating the REST call)

            If the User's time zone is not set then the system time is taken for reference to convert
            to UTC.
        body (UpdateIncidentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateIncidentResponse]
    """

    return sync_detailed(
        incident_id=incident_id,
        incident_id_lookup=incident_id_lookup,
        client=client,
        body=body,
        sysparm_input_display_value=sysparm_input_display_value,
    ).parsed


async def asyncio_detailed(
    incident_id_lookup: Any,
    incident_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateIncidentRequest,
    sysparm_input_display_value: Optional[bool] = None,
) -> Response[Union[DefaultError, UpdateIncidentResponse]]:
    """Update Incident

     Update an incident

    Args:
        incident_id (str): Start typing the incident number to find the incident that needs to be
            updated
        sysparm_input_display_value (Optional[bool]): ServiceNow REST API stores the date-time in
            the UTC time zone unless you specify sysparm_input_display_value to true.

            If you specify sysparm_input_display_value to true, then the date-time is stored exactly
            what you sent in the request.

            If not, the date-time sent via REST API is converted to the UTC time based on the User's
            timezone(User initiating the REST call)

            If the User's time zone is not set then the system time is taken for reference to convert
            to UTC.
        body (UpdateIncidentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, UpdateIncidentResponse]]
    """

    if not incident_id and incident_id_lookup:
        filter = incident_id_lookup
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url=f"/incident?where=number like '{filter}'"
        )
        lookup_response = lookup_response_raw.json()

        found_items = lookup_response

        if not found_items:
            raise ValueError("No matches found for incident_id_lookup in incident")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for incident_id_lookup in incident. Using the first match."
            )

        incident_id = found_items[0]["sys_id"]

    kwargs = _get_kwargs(
        incident_id=incident_id,
        body=body,
        sysparm_input_display_value=sysparm_input_display_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    incident_id_lookup: Any,
    incident_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateIncidentRequest,
    sysparm_input_display_value: Optional[bool] = None,
) -> Optional[Union[DefaultError, UpdateIncidentResponse]]:
    """Update Incident

     Update an incident

    Args:
        incident_id (str): Start typing the incident number to find the incident that needs to be
            updated
        sysparm_input_display_value (Optional[bool]): ServiceNow REST API stores the date-time in
            the UTC time zone unless you specify sysparm_input_display_value to true.

            If you specify sysparm_input_display_value to true, then the date-time is stored exactly
            what you sent in the request.

            If not, the date-time sent via REST API is converted to the UTC time based on the User's
            timezone(User initiating the REST call)

            If the User's time zone is not set then the system time is taken for reference to convert
            to UTC.
        body (UpdateIncidentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, UpdateIncidentResponse]
    """

    return (
        await asyncio_detailed(
            incident_id=incident_id,
            incident_id_lookup=incident_id_lookup,
            client=client,
            body=body,
            sysparm_input_display_value=sysparm_input_display_value,
        )
    ).parsed
