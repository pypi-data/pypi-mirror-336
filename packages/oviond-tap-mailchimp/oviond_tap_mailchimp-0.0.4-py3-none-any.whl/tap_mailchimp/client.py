"""REST client handling, including MailchimpStream base class."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class MailchimpStream(RESTStream):
    """Mailchimp stream class."""

    records_jsonpath = "$[*]"
    next_page_token_jsonpath = "$.next_page"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""

        data_center = self.config["data_center"]

        return "https://{data_center}.api.mailchimp.com/3.0"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config["access_token"],
        )

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = {"count": 1000}

        if next_page_token:
            params["offset"] = next_page_token

        return params

    def get_next_page_token(
        self, response: requests.Response, previous_token: t.Any | None
    ) -> t.Any | None:
        """Extract the next page token from the response."""
        response_json = response.json()
        total_items = response_json.get("total_items", 0)
        current_offset = previous_token or 0
        current_count = len(response_json.get(self.records_jsonpath, []))

        if current_offset + current_count < total_items:
            return current_offset + current_count

        return None

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        account_id = self.config["account_id"]

        for record in extract_jsonpath(self.records_jsonpath, input=response.json()):
            yield {**record, "profile_id": account_id}
