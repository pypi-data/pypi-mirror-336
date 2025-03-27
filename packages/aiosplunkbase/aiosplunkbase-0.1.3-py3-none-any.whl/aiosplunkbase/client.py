from asyncio import run
from typing import AsyncGenerator, Any

from httpx import AsyncClient, AsyncHTTPTransport, Response
from packaging import version

from .exceptions import (
    ApiException,
    AppNotFound,
    NoReleaseFound,
    VersionNotFound,
    AuthenticationError,
)


async def hook(response: Response) -> None:
    """
    If the response is an error, synchronously read the response body before raising.
    This is necessary because the response body is not immediately available when
    streaming.
    """
    if response.is_error:
        await response.aread()
        raise ApiException(response)


class SBClient:
    """
    Splunkbase API client for interacting with Splunk's Splunkbase API.

    Provides methods for authentication, app information retrieval, and app downloads.
    """

    BASE_URL = "https://splunkbase.splunk.com"
    DEFAULT_TIMEOUT = 30.0
    MAX_RETRIES = 5

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

        transport = AsyncHTTPTransport(retries=self.MAX_RETRIES)
        self.httpx_client = AsyncClient(
            transport=transport,
            base_url=self.BASE_URL,
            event_hooks={"response": [hook]},
            timeout=self.DEFAULT_TIMEOUT,
        )

    async def login(self) -> None:
        try:
            await self.request(
                "POST",
                "/api/account:login",
                data={"username": self.username, "password": self.password},
            )
        except ApiException as e:
            if e.status_code == 401:
                raise AuthenticationError("Invalid credentials") from e
            raise

    async def request(self, *args: Any, **kwargs: Any) -> Response:
        response = await self.httpx_client.request(*args, **kwargs)
        return response

    async def search(
        self, query: str, limit: int = 18, product: str = "splunk"
    ) -> dict[str, Any]:
        params = {
            "query": query,
            "limit": limit,
            "product": product,
            "product_types": "enterprise",
            "order": "relevance",
            "include": "display_author,icon,categories,support,rating",
        }
        response = await self.request("GET", "/api/v2/apps", params=params)
        return response.json()

    async def get_app_numeric_id(self, app_name: str) -> str | None:
        """
        This is the only known reliable way to resolve an app name to an ID. Splunkbase
        will redirect to the app page. I sure hope they don't change this.
        """
        try:
            response = await self.httpx_client.request("GET", f"/apps/id/{app_name}")
        except ApiException as http_exc:
            if http_exc.status_code == 404:
                return None
            else:
                raise

        if response.status_code == 302:
            return response.headers["Location"].split("/")[-1]

        else:
            raise ApiException(response)

    async def get_app_info(self, app: int | str) -> dict[str, Any] | None:
        """
        Get app info for an given app ID (non-numeric).
        """
        if isinstance(app, str):
            app_id = await self.get_app_numeric_id(app)
            if app_id is None:
                return None
        else:
            app_id = app

        try:
            response = await self.request(
                "GET",
                f"/api/v1/app/{app_id}/",
                params={"include": "release,releases,releases.splunk_compatibility"},
            )
        except ApiException:
            # Didn't find the app
            return None

        return response.json()

    async def get_app_latest_version(
        self, app: str | int, splunk_version: str, is_cloud: bool | None = None
    ) -> dict[str, Any]:
        """
        Given a list of Splunk versions, find the latest compatible app version.
        """
        app_info = await self.get_app_info(app)
        if app_info is None:
            raise AppNotFound

        if not splunk_version:
            release = app_info.get("release", None)
        else:
            release = None
            releases = sorted(
                app_info.get("releases", []),
                key=lambda release: version.parse(release["title"]),
                reverse=True,
            )

            for potential_release in releases:
                if await self.release_is_compatible(
                    potential_release, splunk_version, is_cloud=is_cloud
                ):
                    release = potential_release
                    break

        if release is None:
            raise NoReleaseFound

        return release

    @staticmethod
    async def release_is_compatible(
        potential_release: dict[str, Any],
        splunk_version: str,
        is_cloud: bool | None = None,
    ) -> bool:
        """
        Check if a release is compatible with a given Splunk version.
        """
        if (
            is_cloud
            and "Splunk Cloud" not in potential_release["product_compatibility"]
        ):
            return False
        for compatible_version in potential_release["splunk_compatibility"]:
            if splunk_version == compatible_version or splunk_version.startswith(
                f"{compatible_version}."
            ):
                return True
        return False

    async def download_app(
        self, app: str | int, app_version: str | None = None
    ) -> AsyncGenerator[bytes, None]:
        """
        Download an app from Splunkbase. If no app_version is provided, the latest
        release will be downloaded.
        """
        data = await self.get_app_info(app)

        if data is None:
            raise AppNotFound

        if app_version is None:
            release = data.get("release", None)

            if release is None:
                raise NoReleaseFound
        else:
            release = None
            for potential_release in data["releases"]:
                if potential_release["title"] == app_version:
                    release = potential_release
                    break

            if release is None:
                raise VersionNotFound

        app_data: dict[str, str] = {}

        for checksum_type in ("sha256", "md5"):
            if checksum_type in release:
                app_data["checksum"] = release[checksum_type]
                break

        async with self.httpx_client.stream(
            "GET", release["path"], follow_redirects=True
        ) as r:
            if not 200 <= r.status_code <= 299:
                raise ApiException(r)
            async for chunk in r.aiter_bytes():
                yield chunk

    async def get_app_supported_versions(self, app: str | int) -> list[str]:
        """
        Get a list of all supported Splunk versions for an app.
        """
        app_info = await self.get_app_info(app)
        if app_info is None:
            raise AppNotFound

        releases = sorted(
            app_info.get("releases", []),
            key=lambda release: version.parse(release["title"]),
            reverse=True,
        )

        splunk_versions = set()
        for release in releases:
            for splunk_version in release["splunk_compatibility"]:
                splunk_versions.add(splunk_version)

        splunk_versions_list = sorted(splunk_versions, key=version.parse)

        return splunk_versions_list

    async def close(self) -> None:
        await self.httpx_client.aclose()

    async def __aenter__(self) -> "SBClient":
        return self

    async def __aexit__(
        self,
        _exc_type,
        _exc_value,
        _traceback,
    ) -> None:
        await self.close()

    def __exit__(
        self,
        _exc_type,
        _exc_value,
        _traceback,
    ) -> None:
        run(self.close())
