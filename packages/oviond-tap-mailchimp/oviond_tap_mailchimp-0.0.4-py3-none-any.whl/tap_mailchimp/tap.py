"""Mailchimp tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th
from tap_mailchimp import streams


class TapMailchimp(Tap):
    """Mailchimp tap class."""

    name = "tap-mailchimp"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            secret=True,
            title="Access Token",
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "data_center",
            th.StringType,
            required=True,
            title="Data Center",
            description="Project IDs to replicate",
        ),
        th.Property(
            "account_id",
            th.StringType,
            required=True,
            title="Account ID",
            description="Project IDs to replicate",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.MailchimpStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CampaignsStream(self),
            streams.AudiencesStream(self),
            streams.AutomationsStream(self),
        ]


if __name__ == "__main__":
    TapMailchimp.cli()
