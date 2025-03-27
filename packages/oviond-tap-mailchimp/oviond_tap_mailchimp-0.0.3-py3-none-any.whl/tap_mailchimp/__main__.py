"""Mailchimp entry point."""

from __future__ import annotations

from tap_mailchimp.tap import TapMailchimp

TapMailchimp.cli()
