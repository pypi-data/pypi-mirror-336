from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.add_comment_request import AddCommentRequest
from ...models.add_comment_response import AddCommentResponse
from ...models.default_error import DefaultError


def _get_kwargs(
    issue_id_or_key: str,
    *,
    body: AddCommentRequest,
    expand: Optional[str] = None,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["expand"] = expand

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/issue/{issue_id_or_key}/comment".format(
            issue_id_or_key=issue_id_or_key,
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
) -> Optional[Union[AddCommentResponse, DefaultError]]:
    if response.status_code == 200:
        response_200 = AddCommentResponse.from_dict(response.json())

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
) -> Response[Union[AddCommentResponse, DefaultError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    issue_id_or_key_lookup: Any,
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AddCommentRequest,
    expand: Optional[str] = None,
) -> Response[Union[AddCommentResponse, DefaultError]]:
    """Add Comment

     Adds a new comment on an issue in Jira

    Args:
        issue_id_or_key (str): The issue key (ABCD-1234) or issue ID
        expand (Optional[str]): Use [expand](#expansion) to include additional information about
            comments in the response. This parameter accepts `renderedBody`, which returns the comment
            body rendered in HTML.
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddCommentResponse, DefaultError]]
    """

    if not issue_id_or_key and issue_id_or_key_lookup:
        filter = issue_id_or_key_lookup
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url=f"/issue/picker?query={filter}"
        )
        lookup_response = lookup_response_raw.json()

        found_items = lookup_response

        if not found_items:
            raise ValueError(
                "No matches found for issue_id_or_key_lookup in issue_picker"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for issue_id_or_key_lookup in issue_picker. Using the first match."
            )

        issue_id_or_key = found_items[0]["key"]

    kwargs = _get_kwargs(
        issue_id_or_key=issue_id_or_key,
        body=body,
        expand=expand,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    issue_id_or_key_lookup: Any,
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AddCommentRequest,
    expand: Optional[str] = None,
) -> Optional[Union[AddCommentResponse, DefaultError]]:
    """Add Comment

     Adds a new comment on an issue in Jira

    Args:
        issue_id_or_key (str): The issue key (ABCD-1234) or issue ID
        expand (Optional[str]): Use [expand](#expansion) to include additional information about
            comments in the response. This parameter accepts `renderedBody`, which returns the comment
            body rendered in HTML.
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddCommentResponse, DefaultError]
    """

    return sync_detailed(
        issue_id_or_key=issue_id_or_key,
        issue_id_or_key_lookup=issue_id_or_key_lookup,
        client=client,
        body=body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    issue_id_or_key_lookup: Any,
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AddCommentRequest,
    expand: Optional[str] = None,
) -> Response[Union[AddCommentResponse, DefaultError]]:
    """Add Comment

     Adds a new comment on an issue in Jira

    Args:
        issue_id_or_key (str): The issue key (ABCD-1234) or issue ID
        expand (Optional[str]): Use [expand](#expansion) to include additional information about
            comments in the response. This parameter accepts `renderedBody`, which returns the comment
            body rendered in HTML.
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddCommentResponse, DefaultError]]
    """

    if not issue_id_or_key and issue_id_or_key_lookup:
        filter = issue_id_or_key_lookup
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url=f"/issue/picker?query={filter}"
        )
        lookup_response = lookup_response_raw.json()

        found_items = lookup_response

        if not found_items:
            raise ValueError(
                "No matches found for issue_id_or_key_lookup in issue_picker"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for issue_id_or_key_lookup in issue_picker. Using the first match."
            )

        issue_id_or_key = found_items[0]["key"]

    kwargs = _get_kwargs(
        issue_id_or_key=issue_id_or_key,
        body=body,
        expand=expand,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    issue_id_or_key_lookup: Any,
    issue_id_or_key: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AddCommentRequest,
    expand: Optional[str] = None,
) -> Optional[Union[AddCommentResponse, DefaultError]]:
    """Add Comment

     Adds a new comment on an issue in Jira

    Args:
        issue_id_or_key (str): The issue key (ABCD-1234) or issue ID
        expand (Optional[str]): Use [expand](#expansion) to include additional information about
            comments in the response. This parameter accepts `renderedBody`, which returns the comment
            body rendered in HTML.
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddCommentResponse, DefaultError]
    """

    return (
        await asyncio_detailed(
            issue_id_or_key=issue_id_or_key,
            issue_id_or_key_lookup=issue_id_or_key_lookup,
            client=client,
            body=body,
            expand=expand,
        )
    ).parsed
