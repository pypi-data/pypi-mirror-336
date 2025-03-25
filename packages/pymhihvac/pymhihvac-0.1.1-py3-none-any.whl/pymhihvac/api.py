"""Provides an asynchronous API client for interacting with MHI HVAC systems.

This module defines the MHIHVACLocalAPI class, which handles communication
with the local API of MHI HVAC systems. It supports login, fetching data,
and sending commands, including automatic re-authentication and retry
mechanisms for handling session expirations.
"""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
import json
import logging
from typing import Any, TypeVar, cast

import aiohttp

from .const import (
    DEFAULT_RAW_DATA_REQUEST_INDEX,
    DEFAULT_RAW_DATA_REQUEST_METHOD,
    RAW_DATA_REQUEST_KEY_MAPPING,
    RAW_DATA_RESPONSE_KEY_MAPPING,
)
from .utils import format_exception

_LOGGER = logging.getLogger(__name__)

HTTP_HEADERS: dict[str, str] = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "User-Agent": "pymhihvac",
}


class LoginFailedException(Exception):
    """Raised when login to MHI HVAC system fails."""


class NoSessionCookieException(Exception):
    """Raised when login to MHI HVAC system does not return session cookie."""


class ApiCallFailedException(Exception):
    """Raised when sending command to MHI HVAC system fails."""


class SessionExpiredException(Exception):
    """Raised when the session cookie is expired or invalid."""


class SessionNotInitializedException(Exception):
    """Raised when the session cookie is expired or invalid."""


class InvalidGetRawDataPayload(Exception):
    """Raised for invalid payloads for getting raw data."""


class InvalidGetRawDataResponse(Exception):
    """Raised for invalid payloads for getting raw data."""


T = TypeVar("T")


@dataclass
class FilteredGroupData:
    """A dataclass representing filtered group data.

    This dataclass stores a list of groups and a boolean indicating
    whether additional valid groups exist beyond those listed.

    Attributes:
        groups (list[dict[str, Any]]):
            A list of group dictionaries. Each dictionary represents a group
            and contains its associated data.
        extra_valid_groups (bool):
            A boolean flag indicating whether there are valid groups beyond
            those included in the `groups` list. This can be useful for
            pagination or situations where only a subset of groups is
            initially retrieved.

    """

    groups: list[dict[str, Any]]
    extra_valid_groups: bool


def reauth_retry(
    max_retries: int = 3,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """Handle re-authentication and retries for session expiry."""

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        async def wrapper(self: "MHIHVACLocalAPI", *args: Any, **kwargs: Any) -> T:
            for attempt in range(max_retries + 1):
                try:
                    return await func(self, *args, **kwargs)
                except SessionExpiredException as e:
                    if attempt < max_retries:
                        _LOGGER.debug(
                            "Session expired, re-authenticating (attempt %d/%d)",
                            attempt + 1,
                            max_retries,
                        )
                        self._session_cookie = await self._async_login()
                    else:
                        raise ApiCallFailedException(
                            f"Max re-authentication attempts ({max_retries}) reached."
                        ) from e
            raise ApiCallFailedException(
                f"Max re-authentication attempts ({max_retries}) reached."
            )

        return wrapper

    return decorator


def _get_filtered_group_data(
    data: dict, method: str, include_groups: list[str] | None = None
) -> FilteredGroupData:
    """Filter and extract group data from a raw data response.

    This function processes raw data retrieved from an API, extracts relevant group
    information based on the specified method and optional group inclusions, and
    returns a FilteredGroupData object containing the filtered groups and a flag
    indicating if additional valid groups exist.


    Args:
        data (dict): The raw data dictionary retrieved from the API.
        method (str): The method used to retrieve the data ("all" or "block").
        include_groups (list[str] | None): An optional list of group numbers to
            include in the filtered results. If None, all valid groups are included.

    Returns:
        FilteredGroupData: A dataclass containing the filtered list of groups and
            a boolean indicating whether additional valid groups exist.

    Raises:
        InvalidGetRawDataResponse: If the provided method is invalid or if the
            expected keys are not found in the data.

    """
    mapping = RAW_DATA_RESPONSE_KEY_MAPPING.get(method)
    if not mapping:
        raise InvalidGetRawDataResponse(f"Invalid method: {method}")

    payload_key = mapping.get("payload_key")
    value_key = mapping.get("value_key")
    groups: list[dict[str, Any]] = []

    if payload_key not in data:
        raise InvalidGetRawDataResponse(f"Key {payload_key} not found in data")

    # For the "all" method, groups are directly in the value_key ("GroupData")
    if method == "all":
        groups = data[payload_key].get(value_key, [])
    # For the "block" method, groups are nested within each floor's "GroupData"
    elif method == "block":
        floors = data[payload_key].get(value_key, [])
        for floor in floors:
            groups.extend(floor.get("GroupData", []))

    # First, filter out groups with OnOff == "4" or GroupNo == "-1"
    valid_groups = [
        group
        for group in groups
        if group.get("OnOff") != "4" and group.get("GroupNo") != "-1"
    ]

    # Further filter based on include_groups (if provided)
    if include_groups is None or not include_groups:
        filtered_groups = valid_groups
        extra_valid = False
    else:
        filtered_groups = [
            group for group in valid_groups if group.get("GroupNo") in include_groups
        ]
        # Determine if there are any valid groups that were filtered out
        extra_valid = any(
            group.get("GroupNo") not in include_groups for group in valid_groups
        )

    return FilteredGroupData(groups=filtered_groups, extra_valid_groups=extra_valid)


def _build_get_raw_data_payload(method: str, include_index: list[str] | None) -> str:
    """Build the payload for a raw data "Get" request.

    This function constructs the payload string for retrieving raw data from the API.
    It uses the provided method and value to create a JSON formatted payload.

    Args:
        method (str, optional): The method to use for retrieving data. Defaults to "all".
        include_index (str | list[str], optional): The index associated with the method. Defaults to "1".

    Returns:
        str: The JSON formatted payload string.

    Raises:
        InvalidGetRawDataPayload: If the provided method is invalid or the payload cannot be constructed.

    """

    keys = RAW_DATA_REQUEST_KEY_MAPPING.get(method)
    if not keys:
        raise InvalidGetRawDataPayload

    if include_index is None or not include_index:
        include_index = DEFAULT_RAW_DATA_REQUEST_INDEX

    payload_key = keys.get("payload_key")
    value_key = keys.get("value_key")

    if payload_key and value_key:
        payload_dict = {payload_key: {value_key: include_index}}
        return f"={json.dumps(payload_dict)}"
    raise InvalidGetRawDataPayload


class MHIHVACLocalAPI:
    """Class to interact with the MHI HVAC local API."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize the API client.

        Args:
            host (str): The HVAC system host or IP address.
            username (str): The username to use for login.
            password (str): The password to use for login.
            session (aiohttp ClientSession): Optional session to use for requests.
                     If None, a new session will be created internally.

        """
        self._username: str = username
        self._password: str = password
        self._api_login_url: str = f"http://{host}/login.asp"
        self._api_url: str = f"http://{host}/json/group_list_json.asp"
        self._session: aiohttp.ClientSession | None = session
        self._session_cookie: str | None = None

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._session_created_internally: bool = (
                True  # Set flag if session was created here
            )
        else:
            self._session_created_internally = (
                False  # Flag session was provided externally
            )

    @property
    def session_cookie(self) -> str | None:
        """Return the cookie of the session."""
        return self._session_cookie

    async def close_session(self) -> None:
        """Close the aiohttp session if it was created internally."""
        if self._session and self._session_created_internally:
            _LOGGER.debug("Closing session")
            await self._session.close()
            self._session = None
            _LOGGER.debug("Session closed")

    @property
    def extra_valid_groups(self) -> bool:
        """Indicates whether additional valid groups exist.

        Returns:
                bool: True if additional valid groups exist, False otherwise.

        """
        return getattr(self, "_extra_valid_groups", False)

    @extra_valid_groups.setter
    def extra_valid_groups(self, value: bool) -> None:
        self._extra_valid_groups = value

    @reauth_retry()
    async def async_get_raw_data(
        self,
        method: str = DEFAULT_RAW_DATA_REQUEST_METHOD,
        include_index: list[str] | None = None,
        include_groups: list[str] | None = None,
    ) -> dict[str, Any]:
        """Fetch data from HVAC system with error handling."""
        if not self._session:
            raise SessionNotInitializedException("Session is not initialized")
        if not self._session_cookie:
            self._session_cookie = await self.async_login()
        headers: dict[str, str] = HTTP_HEADERS.copy()
        headers["Cookie"] = self._session_cookie
        payload: str = _build_get_raw_data_payload(
            method=method, include_index=include_index
        )
        try:
            async with asyncio.timeout(10):
                async with self._session.post(
                    self._api_url, data=payload, headers=headers
                ) as resp:
                    resp_text: str = await resp.text()
                    raw_data: dict[str, Any] = json.loads(resp_text)
                    result = _get_filtered_group_data(
                        data=raw_data, method=method, include_groups=include_groups
                    )
                    if result.groups:
                        self.extra_valid_groups = result.extra_valid_groups
                        return cast(dict[str, Any], result.groups)
                    raise SessionExpiredException
        except (aiohttp.ClientError, TimeoutError, json.JSONDecodeError) as e:
            _LOGGER.error("Error fetching data: %s", format_exception(e))
            raise

    async def async_set_group_property(
        self, group_no: str, properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Wrap the given payload by adding the GroupNo inside SetReqChangeGroup."""
        payload: dict[str, Any] = properties.copy()
        payload.setdefault("GroupNo", group_no)
        payload = {"SetReqChangeGroup": payload}
        return await self._async_send_command(payload)

    async def async_set_all_property(
        self, properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Wrap the given payload with the SetReqChangeAll key."""
        payload: dict[str, Any] = {"SetReqChangeAll": properties.copy()}
        return await self._async_send_command(payload)

    @reauth_retry()
    async def _async_send_command(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a command to the API asynchronously with limited re-authentication attempts."""
        if not self._session:
            raise SessionNotInitializedException("Session is not initialized")
        if not isinstance(payload, dict):
            _LOGGER.error("Payload '%s' is not a dictionary", payload)
            return {"_async_send_command": "Payload is not a dictionary"}
        headers: dict[str, str] = HTTP_HEADERS.copy()
        data: str = f"={json.dumps(payload)}"
        if self._session_cookie:
            headers["Cookie"] = self._session_cookie
        try:
            async with asyncio.timeout(10):
                _LOGGER.debug("Sending command: %s", data)
                async with self._session.post(
                    self._api_url,
                    data=data,
                    headers=headers,
                ) as resp:
                    resp_text: str = await resp.text()
                    if resp.status != 200:
                        raise ApiCallFailedException(
                            f"Command failed with HTTP {resp.status}."
                        )
                    if not resp_text.strip():
                        raise SessionExpiredException
                    return cast(dict[str, Any], json.loads(resp_text))
                return resp_text
        except (aiohttp.ClientError, TimeoutError) as e:
            _LOGGER.error("Command failed with error: %s", format_exception(e))
            raise

    async def async_login(self) -> str:
        """Login to the HVAC system and return the session cookie.

        Performs a login via the HVAC's /login.asp endpoint using the provided
        credentials. Returns the session cookie if successful.

        Returns:
            A string containing the session cookie.

        Raises:
            Exception: If login fails or no cookie is returned.

        """
        return await self._async_login()

    async def _async_login(self) -> str:
        """Login to the HVAC system and return the session cookie.

        Internal method to perform the login.
        """
        if not self._session:
            raise SessionNotInitializedException("Session is not initialized")
        headers: dict[str, str] = HTTP_HEADERS.copy()
        data: dict[str, str] = {"Id": self._username, "Password": self._password}
        try:
            async with (
                asyncio.timeout(10),
                self._session.post(
                    self._api_login_url,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                ) as resp,
            ):
                if resp.status != 302:
                    raise LoginFailedException(
                        f"Login failed with status {resp.status}"
                    )
                cookie: str | None = resp.headers.get("Set-Cookie")
                if not cookie:
                    raise NoSessionCookieException(
                        "Login did not return a session cookie"
                    )
                _LOGGER.debug("Logged in, session cookie: %s", cookie)
                return cookie
        except (aiohttp.ClientError, TimeoutError) as e:
            _LOGGER.error("Login error: %s", format_exception(e))
            raise
