# Copyright Gustav Ebbers
from enum import Enum

import requests
from loguru import logger

from .models import Member

HTTP_TIMEOUT_SECONDS = 10


class SDK:
    def __init__(self, api_url: str, api_key: str, api_secret: str) -> None:
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret

    class MemberSortOrder(str, Enum):
        DESC = "desc"
        ASC = "asc"

    def list_members(self, ordering: str = MemberSortOrder.DESC, search: str = None) -> [Member]:
        params = {"ordering": ordering, "page": 1}

        if search is not None:
            params["search"] = search

        members = []

        while True:
            try:
                r = requests.get(
                    self.api_url + "members",
                    headers={
                        "api-key": self.api_key,
                        "api_secret": self.api_secret,
                    },
                    params=params,
                    timeout=HTTP_TIMEOUT_SECONDS,
                )
                r.raise_for_status()
            except requests.exceptions.ConnectionError as err:
                raise ValueError("Connection error, check `GlowSDK.api_url` is set correctly") from err
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 403:
                    raise ValueError(
                        "Authentication error, check `GlowSDK.api_key` and `GlowSDK.api_secret` are set correctly"
                    ) from err
                else:
                    raise

            members += [Member(**member) for member in r.json()["data"]]

            logger.debug(
                f"Retrieved {len(r.json()['data'])} members of {r.json()['total']} from Glow API on page {r.json()['current_page']}/{r.json()['last_page']}"
            )

            if r.json()["next_page_url"] is None:
                break

            params["page"] = params["page"] + 1

        return members

    def get_member(
        self,
        member_id: int | None = None,
        email: str | None = None,
        platform_id: int | None = None,
    ) -> Member:
        if not (member_id or email or platform_id):
            raise ValueError("`member_id` or `email` or `platform_id` is required")

        params = {}
        if member_id:
            params["id"] = member_id
        elif email:
            params["email"] = email
        elif platform_id:
            params["platform_id"] = platform_id

        try:
            r = requests.get(
                self.api_url + "member",
                headers={
                    "api-key": self.api_key,
                    "api_secret": self.api_secret,
                },
                params=params,
                timeout=HTTP_TIMEOUT_SECONDS,
            )
            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `GlowSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `GlowSDK.api_key` and `GlowSDK.api_secret` are set correctly"
                ) from err
            else:
                raise

        return Member(**r.json())

    def delete_member(self, member: Member | None = None, member_id: int | None = None):
        if not (member_id or member):
            raise ValueError("`member` or `member_id` is required")

        params = {}
        if member:
            params["id"] = member.id
        elif member_id:
            params["id"] = member_id

        try:
            r = requests.post(
                self.api_url + "delete-member",
                headers={
                    "api-key": self.api_key,
                    "api_secret": self.api_secret,
                },
                params=params,
                timeout=HTTP_TIMEOUT_SECONDS,
            )
            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `GlowSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `GlowSDK.api_key` and `GlowSDK.api_secret` are set correctly"
                ) from err
            else:
                raise

    def update_member_points(self, point_balance: int, member: Member | None = None, member_id: int | None = None):
        if not (member_id or member):
            raise ValueError("`member` or `member_id` is required")

        params = {
            "point_balance": point_balance,
        }
        if member:
            params["id"] = member.id
        elif member_id:
            params["id"] = member_id

        try:
            r = requests.post(
                self.api_url + "update-member",
                headers={
                    "api-key": self.api_key,
                    "api_secret": self.api_secret,
                },
                params=params,
                timeout=HTTP_TIMEOUT_SECONDS,
            )
            r.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise ValueError("Connection error, check `GlowSDK.api_url` is set correctly") from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise ValueError(
                    "Authentication error, check `GlowSDK.api_key` and `GlowSDK.api_secret` are set correctly"
                ) from err
            else:
                raise
