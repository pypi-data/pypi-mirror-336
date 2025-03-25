from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError


def _get_kwargs(
    id: str,
    *,
    wipe_data: Optional[bool] = None,
    keep_account: Optional[bool] = None,
    transfer_admin_id: Optional[str] = None,
    transfer_dest_id: Optional[str] = None,
    retain_team_shares: Optional[bool] = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["wipe_data"] = wipe_data

    params["keep_account"] = keep_account

    params["transfer_admin_id"] = transfer_admin_id

    params["transfer_dest_id"] = transfer_dest_id

    params["retain_team_shares"] = retain_team_shares

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/members/{id}".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DefaultError]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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
) -> Response[Union[Any, DefaultError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id_lookup: Any,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    wipe_data: Optional[bool] = None,
    keep_account: Optional[bool] = None,
    transfer_admin_id: Optional[str] = None,
    transfer_dest_id: Optional[str] = None,
    retain_team_shares: Optional[bool] = None,
) -> Response[Union[Any, DefaultError]]:
    """Remove a Member

      Remove a member from a team

    Args:
        id (str): ID of the member
        wipe_data (Optional[bool]): If provided, controls if the user's data will be deleted on
            their linked devices. The default for this field is True.Valid values are true/false
        keep_account (Optional[bool]): In order to keep the account the argument wipe_data should
            be set to false. The default for this field is False.Valid values are true/false
        transfer_admin_id (Optional[str]):  If provided, errors during the transfer process will
            be sent via email to this user. If the transfer_dest_id argument was provided, then this
            argument must be provided as well.
        transfer_dest_id (Optional[str]): If provided, files from the deleted member account will
            be transferred to this user.
        retain_team_shares (Optional[bool]): In order to keep the sharing relationships, the
            arguments wipe_data should be set to false and keep_account should be set to true.Valid
            values are true/false

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    if not id and id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/members"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if id_lookup in item["profile.email"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for id_lookup in members")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for id_lookup in members. Using the first match."
            )

        id = found_items[0]["profile.team_member_id"]

    kwargs = _get_kwargs(
        id=id,
        wipe_data=wipe_data,
        keep_account=keep_account,
        transfer_admin_id=transfer_admin_id,
        transfer_dest_id=transfer_dest_id,
        retain_team_shares=retain_team_shares,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id_lookup: Any,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    wipe_data: Optional[bool] = None,
    keep_account: Optional[bool] = None,
    transfer_admin_id: Optional[str] = None,
    transfer_dest_id: Optional[str] = None,
    retain_team_shares: Optional[bool] = None,
) -> Optional[Union[Any, DefaultError]]:
    """Remove a Member

      Remove a member from a team

    Args:
        id (str): ID of the member
        wipe_data (Optional[bool]): If provided, controls if the user's data will be deleted on
            their linked devices. The default for this field is True.Valid values are true/false
        keep_account (Optional[bool]): In order to keep the account the argument wipe_data should
            be set to false. The default for this field is False.Valid values are true/false
        transfer_admin_id (Optional[str]):  If provided, errors during the transfer process will
            be sent via email to this user. If the transfer_dest_id argument was provided, then this
            argument must be provided as well.
        transfer_dest_id (Optional[str]): If provided, files from the deleted member account will
            be transferred to this user.
        retain_team_shares (Optional[bool]): In order to keep the sharing relationships, the
            arguments wipe_data should be set to false and keep_account should be set to true.Valid
            values are true/false

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return sync_detailed(
        id=id,
        id_lookup=id_lookup,
        client=client,
        wipe_data=wipe_data,
        keep_account=keep_account,
        transfer_admin_id=transfer_admin_id,
        transfer_dest_id=transfer_dest_id,
        retain_team_shares=retain_team_shares,
    ).parsed


async def asyncio_detailed(
    id_lookup: Any,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    wipe_data: Optional[bool] = None,
    keep_account: Optional[bool] = None,
    transfer_admin_id: Optional[str] = None,
    transfer_dest_id: Optional[str] = None,
    retain_team_shares: Optional[bool] = None,
) -> Response[Union[Any, DefaultError]]:
    """Remove a Member

      Remove a member from a team

    Args:
        id (str): ID of the member
        wipe_data (Optional[bool]): If provided, controls if the user's data will be deleted on
            their linked devices. The default for this field is True.Valid values are true/false
        keep_account (Optional[bool]): In order to keep the account the argument wipe_data should
            be set to false. The default for this field is False.Valid values are true/false
        transfer_admin_id (Optional[str]):  If provided, errors during the transfer process will
            be sent via email to this user. If the transfer_dest_id argument was provided, then this
            argument must be provided as well.
        transfer_dest_id (Optional[str]): If provided, files from the deleted member account will
            be transferred to this user.
        retain_team_shares (Optional[bool]): In order to keep the sharing relationships, the
            arguments wipe_data should be set to false and keep_account should be set to true.Valid
            values are true/false

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DefaultError]]
    """

    if not id and id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/members"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if id_lookup in item["profile.email"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for id_lookup in members")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for id_lookup in members. Using the first match."
            )

        id = found_items[0]["profile.team_member_id"]

    kwargs = _get_kwargs(
        id=id,
        wipe_data=wipe_data,
        keep_account=keep_account,
        transfer_admin_id=transfer_admin_id,
        transfer_dest_id=transfer_dest_id,
        retain_team_shares=retain_team_shares,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id_lookup: Any,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    wipe_data: Optional[bool] = None,
    keep_account: Optional[bool] = None,
    transfer_admin_id: Optional[str] = None,
    transfer_dest_id: Optional[str] = None,
    retain_team_shares: Optional[bool] = None,
) -> Optional[Union[Any, DefaultError]]:
    """Remove a Member

      Remove a member from a team

    Args:
        id (str): ID of the member
        wipe_data (Optional[bool]): If provided, controls if the user's data will be deleted on
            their linked devices. The default for this field is True.Valid values are true/false
        keep_account (Optional[bool]): In order to keep the account the argument wipe_data should
            be set to false. The default for this field is False.Valid values are true/false
        transfer_admin_id (Optional[str]):  If provided, errors during the transfer process will
            be sent via email to this user. If the transfer_dest_id argument was provided, then this
            argument must be provided as well.
        transfer_dest_id (Optional[str]): If provided, files from the deleted member account will
            be transferred to this user.
        retain_team_shares (Optional[bool]): In order to keep the sharing relationships, the
            arguments wipe_data should be set to false and keep_account should be set to true.Valid
            values are true/false

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DefaultError]
    """

    return (
        await asyncio_detailed(
            id=id,
            id_lookup=id_lookup,
            client=client,
            wipe_data=wipe_data,
            keep_account=keep_account,
            transfer_admin_id=transfer_admin_id,
            transfer_dest_id=transfer_dest_id,
            retain_team_shares=retain_team_shares,
        )
    ).parsed
