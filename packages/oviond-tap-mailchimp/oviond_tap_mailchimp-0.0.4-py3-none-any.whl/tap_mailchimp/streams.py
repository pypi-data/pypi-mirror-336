"""Stream type classes for tap-mailchimp."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_mailchimp.client import MailchimpStream


class CampaignsStream(MailchimpStream):
    """Define custom stream."""

    name = "mailchimp_campaigns"
    path = "/reports"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.reports[*]"
    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="Unique ID of the report"),
        th.Property(
            "campaign_title", th.StringType, description="Title of the campaign"
        ),
        th.Property("type", th.StringType, description="Type of the report"),
        th.Property("list_id", th.StringType, description="List ID"),
        th.Property(
            "list_is_active", th.BooleanType, description="Whether the list is active"
        ),
        th.Property("list_name", th.StringType, description="Name of the list"),
        th.Property(
            "subject_line", th.StringType, description="Subject line of the report"
        ),
        th.Property(
            "preview_text", th.StringType, description="Preview text of the report"
        ),
        th.Property("emails_sent", th.IntegerType, description="Number of emails sent"),
        th.Property(
            "abuse_reports", th.IntegerType, description="Number of abuse reports"
        ),
        th.Property(
            "unsubscribed", th.IntegerType, description="Number of unsubscribed users"
        ),
        th.Property("send_time", th.StringType, description="Send time of the report"),
        th.Property("rss_last_send", th.StringType, description="Last RSS send time"),
        th.Property(
            "bounces",
            th.ObjectType(
                th.Property(
                    "hard_bounces", th.IntegerType, description="Number of hard bounces"
                ),
                th.Property(
                    "soft_bounces", th.IntegerType, description="Number of soft bounces"
                ),
                th.Property(
                    "syntax_errors",
                    th.IntegerType,
                    description="Number of syntax errors",
                ),
            ),
        ),
        th.Property(
            "forwards",
            th.ObjectType(
                th.Property(
                    "forwards_count", th.IntegerType, description="Number of forwards"
                ),
                th.Property(
                    "forwards_opens",
                    th.IntegerType,
                    description="Number of opens from forwards",
                ),
            ),
        ),
        th.Property(
            "opens",
            th.ObjectType(
                th.Property("opens_total", th.IntegerType, description="Total opens"),
                th.Property("unique_opens", th.IntegerType, description="Unique opens"),
                th.Property(
                    "open_rate", th.NumberType, description="Open rate percentage"
                ),
                th.Property(
                    "last_open", th.StringType, description="Timestamp of last open"
                ),
            ),
        ),
        th.Property(
            "clicks",
            th.ObjectType(
                th.Property("clicks_total", th.IntegerType, description="Total clicks"),
                th.Property(
                    "unique_clicks", th.IntegerType, description="Unique clicks"
                ),
                th.Property(
                    "unique_subscriber_clicks",
                    th.IntegerType,
                    description="Unique subscriber clicks",
                ),
                th.Property(
                    "click_rate", th.NumberType, description="Click rate percentage"
                ),
                th.Property(
                    "last_click", th.StringType, description="Timestamp of last click"
                ),
            ),
        ),
        th.Property(
            "facebook_likes",
            th.ObjectType(
                th.Property(
                    "recipient_likes", th.IntegerType, description="Recipient likes"
                ),
                th.Property("unique_likes", th.IntegerType, description="Unique likes"),
                th.Property(
                    "facebook_likes", th.IntegerType, description="Total Facebook likes"
                ),
            ),
        ),
        th.Property(
            "industry_stats",
            th.ObjectType(
                th.Property("type", th.StringType, description="Industry type"),
                th.Property(
                    "open_rate", th.NumberType, description="Industry open rate"
                ),
                th.Property(
                    "click_rate", th.NumberType, description="Industry click rate"
                ),
                th.Property(
                    "bounce_rate", th.NumberType, description="Industry bounce rate"
                ),
                th.Property(
                    "unopen_rate", th.NumberType, description="Industry unopen rate"
                ),
                th.Property(
                    "unsub_rate", th.NumberType, description="Industry unsubscribe rate"
                ),
                th.Property(
                    "abuse_rate", th.NumberType, description="Industry abuse rate"
                ),
            ),
        ),
        th.Property(
            "list_stats",
            th.ObjectType(
                th.Property("sub_rate", th.NumberType, description="Subscription rate"),
                th.Property(
                    "unsub_rate", th.NumberType, description="Unsubscription rate"
                ),
                th.Property("open_rate", th.NumberType, description="Open rate"),
                th.Property("click_rate", th.NumberType, description="Click rate"),
            ),
        ),
        th.Property(
            "ab_split",
            th.ObjectType(
                th.Property(
                    "a",
                    th.ObjectType(
                        th.Property(
                            "bounces", th.IntegerType, description="Bounces for group A"
                        ),
                        th.Property(
                            "abuse_reports",
                            th.IntegerType,
                            description="Abuse reports for group A",
                        ),
                        th.Property(
                            "unsubs",
                            th.IntegerType,
                            description="Unsubscriptions for group A",
                        ),
                        th.Property(
                            "recipient_clicks",
                            th.IntegerType,
                            description="Clicks for group A",
                        ),
                        th.Property(
                            "forwards",
                            th.IntegerType,
                            description="Forwards for group A",
                        ),
                        th.Property(
                            "forwards_opens",
                            th.IntegerType,
                            description="Opens from forwards for group A",
                        ),
                        th.Property(
                            "opens", th.IntegerType, description="Opens for group A"
                        ),
                        th.Property(
                            "last_open",
                            th.StringType,
                            description="Last open timestamp for group A",
                        ),
                        th.Property(
                            "unique_opens",
                            th.IntegerType,
                            description="Unique opens for group A",
                        ),
                    ),
                ),
                th.Property(
                    "b",
                    th.ObjectType(
                        th.Property(
                            "bounces", th.IntegerType, description="Bounces for group B"
                        ),
                        th.Property(
                            "abuse_reports",
                            th.IntegerType,
                            description="Abuse reports for group B",
                        ),
                        th.Property(
                            "unsubs",
                            th.IntegerType,
                            description="Unsubscriptions for group B",
                        ),
                        th.Property(
                            "recipient_clicks",
                            th.IntegerType,
                            description="Clicks for group B",
                        ),
                        th.Property(
                            "forwards",
                            th.IntegerType,
                            description="Forwards for group B",
                        ),
                        th.Property(
                            "forwards_opens",
                            th.IntegerType,
                            description="Opens from forwards for group B",
                        ),
                        th.Property(
                            "opens", th.IntegerType, description="Opens for group B"
                        ),
                        th.Property(
                            "last_open",
                            th.StringType,
                            description="Last open timestamp for group B",
                        ),
                        th.Property(
                            "unique_opens",
                            th.IntegerType,
                            description="Unique opens for group B",
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "timewarp",
            th.ArrayType(
                th.ObjectType(
                    th.Property("gmt_offset", th.IntegerType, description="GMT offset"),
                    th.Property("opens", th.IntegerType, description="Number of opens"),
                    th.Property(
                        "last_open", th.StringType, description="Last open timestamp"
                    ),
                    th.Property(
                        "unique_opens", th.IntegerType, description="Unique opens"
                    ),
                    th.Property(
                        "clicks", th.IntegerType, description="Number of clicks"
                    ),
                    th.Property(
                        "last_click", th.StringType, description="Last click timestamp"
                    ),
                    th.Property(
                        "unique_clicks", th.IntegerType, description="Unique clicks"
                    ),
                    th.Property(
                        "bounces", th.IntegerType, description="Number of bounces"
                    ),
                )
            ),
        ),
        th.Property(
            "timeseries",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "timestamp", th.StringType, description="Timestamp of the event"
                    ),
                    th.Property(
                        "emails_sent",
                        th.IntegerType,
                        description="Emails sent at this timestamp",
                    ),
                    th.Property(
                        "unique_opens",
                        th.IntegerType,
                        description="Unique opens at this timestamp",
                    ),
                    th.Property(
                        "recipients_clicks",
                        th.IntegerType,
                        description="Recipient clicks at this timestamp",
                    ),
                )
            ),
        ),
        th.Property(
            "share_report",
            th.ObjectType(
                th.Property(
                    "share_url", th.StringType, description="URL to share the report"
                ),
                th.Property(
                    "share_password",
                    th.StringType,
                    description="Password to share the report",
                ),
            ),
        ),
        th.Property(
            "ecommerce",
            th.ObjectType(
                th.Property("total_orders", th.IntegerType, description="Total orders"),
                th.Property(
                    "total_spent", th.NumberType, description="Total amount spent"
                ),
                th.Property(
                    "total_revenue",
                    th.NumberType,
                    description="Total revenue generated",
                ),
                th.Property(
                    "currency_code", th.StringType, description="Currency code"
                ),
            ),
        ),
        th.Property(
            "delivery_status",
            th.ObjectType(
                th.Property(
                    "enabled", th.BooleanType, description="Delivery status enabled"
                ),
                th.Property(
                    "can_cancel", th.BooleanType, description="Can cancel delivery"
                ),
                th.Property("status", th.StringType, description="Delivery status"),
                th.Property("emails_sent", th.IntegerType, description="Emails sent"),
                th.Property(
                    "emails_canceled", th.IntegerType, description="Emails canceled"
                ),
            ),
        ),
        th.Property(
            "_links",
            th.ArrayType(
                th.ObjectType(
                    th.Property("rel", th.StringType, description="Relation type"),
                    th.Property("href", th.StringType, description="URL of the link"),
                    th.Property("method", th.StringType, description="HTTP method"),
                    th.Property(
                        "targetSchema",
                        th.StringType,
                        description="Schema of the target",
                    ),
                    th.Property("schema", th.StringType, description="Schema details"),
                )
            ),
        ),
    ).to_dict()


class AudiencesStream(MailchimpStream):
    """Define custom stream."""

    name = "mailchimp_lists"
    path = "/lists"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.lists[*]"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Unique ID for the list",
        ),
        th.Property(
            "web_id",
            th.IntegerType,
            description="Web ID for the list",
        ),
        th.Property(
            "name",
            th.StringType,
            description="Name of the list",
        ),
        th.Property(
            "contact",
            th.ObjectType(
                th.Property("company", th.StringType, description="Company name"),
                th.Property("address1", th.StringType, description="Address line 1"),
                th.Property("address2", th.StringType, description="Address line 2"),
                th.Property("city", th.StringType, description="City"),
                th.Property("state", th.StringType, description="State"),
                th.Property("zip", th.StringType, description="Postal code"),
                th.Property("country", th.StringType, description="Country"),
                th.Property("phone", th.StringType, description="Phone number"),
            ),
        ),
        th.Property(
            "permission_reminder",
            th.StringType,
            description="Permission reminder text for the list",
        ),
        th.Property(
            "use_archive_bar",
            th.BooleanType,
            description="Whether the archive bar is used",
        ),
        th.Property(
            "campaign_defaults",
            th.ObjectType(
                th.Property(
                    "from_name", th.StringType, description="Default sender name"
                ),
                th.Property(
                    "from_email", th.StringType, description="Default sender email"
                ),
                th.Property(
                    "subject", th.StringType, description="Default subject line"
                ),
                th.Property("language", th.StringType, description="Default language"),
            ),
        ),
        th.Property(
            "notify_on_subscribe",
            th.BooleanType,
            description="Whether notifications are sent on subscription",
        ),
        th.Property(
            "notify_on_unsubscribe",
            th.BooleanType,
            description="Whether notifications are sent on unsubscription",
        ),
        th.Property(
            "date_created",
            th.StringType,
            description="Date and time when the list was created",
        ),
        th.Property(
            "list_rating",
            th.IntegerType,
            description="The list rating",
        ),
        th.Property(
            "email_type_option",
            th.BooleanType,
            description="Whether the list supports email type options",
        ),
        th.Property(
            "subscribe_url_short",
            th.StringType,
            description="Short URL for subscription",
        ),
        th.Property(
            "subscribe_url_long",
            th.StringType,
            description="Long URL for subscription",
        ),
        th.Property(
            "beamer_address",
            th.StringType,
            description="Beamer address for the list",
        ),
        th.Property(
            "visibility",
            th.StringType,
            description="Visibility of the list (e.g., pub)",
        ),
        th.Property(
            "double_optin",
            th.BooleanType,
            description="Whether double opt-in is enabled",
        ),
        th.Property(
            "has_welcome",
            th.BooleanType,
            description="Whether the list has a welcome email",
        ),
        th.Property(
            "marketing_permissions",
            th.BooleanType,
            description="Whether the list uses marketing permissions",
        ),
        th.Property(
            "modules",
            th.ArrayType(th.StringType),
            description="Modules associated with the list",
        ),
        th.Property(
            "stats",
            th.ObjectType(
                th.Property(
                    "member_count", th.IntegerType, description="Total members"
                ),
                th.Property(
                    "total_contacts", th.IntegerType, description="Total contacts"
                ),
                th.Property(
                    "unsubscribe_count",
                    th.IntegerType,
                    description="Total unsubscribed contacts",
                ),
                th.Property(
                    "cleaned_count",
                    th.IntegerType,
                    description="Total cleaned contacts",
                ),
                th.Property(
                    "member_count_since_send",
                    th.IntegerType,
                    description="Members added since last campaign",
                ),
                th.Property(
                    "unsubscribe_count_since_send",
                    th.IntegerType,
                    description="Unsubscribes since last campaign",
                ),
                th.Property(
                    "cleaned_count_since_send",
                    th.IntegerType,
                    description="Cleaned contacts since last campaign",
                ),
                th.Property(
                    "campaign_count",
                    th.IntegerType,
                    description="Number of campaigns sent to this list",
                ),
                th.Property(
                    "campaign_last_sent",
                    th.StringType,
                    description="Date of the last campaign sent",
                    nullable=True,
                ),
                th.Property(
                    "merge_field_count",
                    th.IntegerType,
                    description="Number of merge fields for the list",
                ),
                th.Property(
                    "avg_sub_rate",
                    th.NumberType,
                    description="Average subscription rate",
                ),
                th.Property(
                    "avg_unsub_rate",
                    th.NumberType,
                    description="Average unsubscription rate",
                ),
                th.Property(
                    "target_sub_rate",
                    th.NumberType,
                    description="Target subscription rate",
                ),
                th.Property("open_rate", th.NumberType, description="Open rate"),
                th.Property("click_rate", th.NumberType, description="Click rate"),
                th.Property(
                    "last_sub_date",
                    th.StringType,
                    description="Last subscription date",
                    nullable=True,
                ),
                th.Property(
                    "last_unsub_date",
                    th.StringType,
                    description="Last unsubscription date",
                    nullable=True,
                ),
            ),
        ),
        th.Property(
            "_links",
            th.ArrayType(
                th.ObjectType(
                    th.Property("rel", th.StringType, description="Relation type"),
                    th.Property("href", th.StringType, description="Link URL"),
                    th.Property("method", th.StringType, description="HTTP method"),
                    th.Property("targetSchema", th.StringType, nullable=True),
                    th.Property("schema", th.StringType, nullable=True),
                ),
            ),
        ),
        th.Property("profile_id", th.StringType),
    ).to_dict()


class AutomationsStream(MailchimpStream):
    """Define custom stream."""

    name = "mailchimp_automations"
    path = "/automations"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.lists[*]"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Unique ID of the automation",
        ),
        th.Property(
            "create_time",
            th.StringType,
            description="Timestamp when the automation was created",
        ),
        th.Property(
            "start_time",
            th.StringType,
            description="Timestamp when the automation started",
        ),
        th.Property(
            "status",
            th.StringType,
            description="Status of the automation",
        ),
        th.Property(
            "emails_sent",
            th.IntegerType,
            description="Number of emails sent by this automation",
        ),
        th.Property(
            "recipients",
            th.ObjectType(
                th.Property("list_id", th.StringType, description="List ID"),
                th.Property(
                    "list_is_active",
                    th.BooleanType,
                    description="Indicates if the list is active",
                ),
                th.Property("list_name", th.StringType, description="Name of the list"),
                th.Property(
                    "segment_opts",
                    th.ObjectType(
                        th.Property(
                            "saved_segment_id",
                            th.IntegerType,
                            description="ID of the saved segment",
                        ),
                        th.Property(
                            "match",
                            th.StringType,
                            description="Match type for segment options",
                        ),
                        th.Property(
                            "conditions",
                            th.ArrayType(th.StringType, nullable=True),
                            description="Conditions for segment options",
                        ),
                    ),
                ),
                th.Property("store_id", th.StringType, description="Store ID"),
            ),
        ),
        th.Property(
            "settings",
            th.ObjectType(
                th.Property(
                    "title", th.StringType, description="Title of the automation"
                ),
                th.Property("from_name", th.StringType, description="Sender's name"),
                th.Property(
                    "reply_to", th.StringType, description="Reply-to email address"
                ),
                th.Property(
                    "use_conversation",
                    th.BooleanType,
                    description="Indicates if conversations are enabled",
                ),
                th.Property("to_name", th.StringType, description="Recipient's name"),
                th.Property(
                    "authenticate",
                    th.BooleanType,
                    description="Indicates if the sender's email is authenticated",
                ),
                th.Property(
                    "auto_footer",
                    th.BooleanType,
                    description="Indicates if auto footers are added",
                ),
                th.Property(
                    "inline_css",
                    th.BooleanType,
                    description="Indicates if inline CSS is applied",
                ),
            ),
        ),
        th.Property(
            "tracking",
            th.ObjectType(
                th.Property(
                    "opens",
                    th.BooleanType,
                    description="Indicates if opens are tracked",
                ),
                th.Property(
                    "html_clicks",
                    th.BooleanType,
                    description="Indicates if HTML clicks are tracked",
                ),
                th.Property(
                    "text_clicks",
                    th.BooleanType,
                    description="Indicates if text clicks are tracked",
                ),
                th.Property(
                    "goal_tracking",
                    th.BooleanType,
                    description="Indicates if goal tracking is enabled",
                ),
                th.Property(
                    "ecomm360",
                    th.BooleanType,
                    description="Indicates if eCommerce360 is enabled",
                ),
                th.Property(
                    "google_analytics",
                    th.StringType,
                    description="Google Analytics tracking ID",
                ),
                th.Property(
                    "clicktale", th.StringType, description="Clicktale tracking ID"
                ),
                th.Property(
                    "salesforce",
                    th.ObjectType(
                        th.Property(
                            "campaign", th.BooleanType, description="Campaign tracking"
                        ),
                        th.Property(
                            "notes", th.BooleanType, description="Notes tracking"
                        ),
                    ),
                ),
                th.Property(
                    "capsule",
                    th.ObjectType(
                        th.Property(
                            "notes",
                            th.BooleanType,
                            description="Capsule notes tracking",
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "trigger_settings",
            th.ObjectType(
                th.Property(
                    "workflow_type",
                    th.StringType,
                    description="Type of the workflow trigger",
                ),
                th.Property(
                    "workflow_title",
                    th.StringType,
                    description="Title of the workflow",
                ),
                th.Property(
                    "runtime",
                    th.ObjectType(
                        th.Property(
                            "days",
                            th.ArrayType(th.StringType),
                            description="Days of the week the workflow runs",
                        ),
                        th.Property(
                            "hours",
                            th.ObjectType(
                                th.Property(
                                    "type",
                                    th.StringType,
                                    description="Type of runtime scheduling",
                                )
                            ),
                        ),
                    ),
                ),
                th.Property(
                    "workflow_emails_count",
                    th.IntegerType,
                    description="Count of emails in the workflow",
                ),
            ),
        ),
        th.Property(
            "report_summary",
            th.ObjectType(
                th.Property(
                    "opens", th.IntegerType, description="Total number of opens"
                ),
                th.Property(
                    "unique_opens",
                    th.IntegerType,
                    description="Number of unique opens",
                ),
                th.Property(
                    "open_rate", th.NumberType, description="Open rate percentage"
                ),
                th.Property(
                    "clicks", th.IntegerType, description="Total number of clicks"
                ),
                th.Property(
                    "subscriber_clicks",
                    th.IntegerType,
                    description="Number of clicks from subscribers",
                ),
                th.Property(
                    "click_rate",
                    th.NumberType,
                    description="Click rate percentage",
                ),
            ),
        ),
        th.Property(
            "_links",
            th.ArrayType(
                th.ObjectType(
                    th.Property("rel", th.StringType, description="Relation type"),
                    th.Property("href", th.StringType, description="Link URL"),
                    th.Property("method", th.StringType, description="HTTP method"),
                    th.Property("targetSchema", th.StringType, nullable=True),
                    th.Property("schema", th.StringType, nullable=True),
                ),
            ),
        ),
        th.Property("profile_id", th.StringType),
    ).to_dict()
