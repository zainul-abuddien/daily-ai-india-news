"""Daily AI + India news email automation.

Run examples:
    python main.py --dry-run
    python main.py --send
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from config import FEEDS
from email_sender import EmailSettings, build_email_body, build_subject, send_email
from weather import get_weather
from news_fetcher import fetch_top_items
from summarizer import create_key_takeaway, summarize_item


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a daily AI + India news email.")
    parser.add_argument("--dry-run", action="store_true", help="Build the email but do not send it.")
    parser.add_argument("--send", action="store_true", help="Send the email through Gmail SMTP.")
    parser.add_argument(
        "--save-preview",
        action="store_true",
        help="Save email_preview.html and email_preview.txt for review.",
    )
    args = parser.parse_args()

    if not args.dry_run and not args.send:
        parser.error("Choose either --dry-run or --send.")

    load_dotenv()

    timezone_name = os.getenv("TIMEZONE", "Asia/Kolkata")
    max_age_hours = _get_int_env("MAX_NEWS_AGE_HOURS", 48)
    today = datetime.now(ZoneInfo(timezone_name)).strftime("%d %B %Y")

    print("Fetching AI news...")
    ai_news = fetch_top_items(FEEDS, "ai", limit=5, max_age_hours=max_age_hours)
    print(f"Found {len(ai_news)} AI items.")

    print("Fetching India news...")
    india_news = fetch_top_items(FEEDS, "india", limit=5, max_age_hours=max_age_hours)
    print(f"Found {len(india_news)} India items.")

    if len(ai_news) < 1 or len(india_news) < 1:
        raise RuntimeError(
            "Not enough news items were found. Try increasing MAX_NEWS_AGE_HOURS or checking the RSS feed URLs."
        )

    ai_summaries = [summarize_item(item) for item in ai_news]
    india_summaries = [summarize_item(item) for item in india_news]
    key_takeaway = create_key_takeaway(ai_summaries, india_summaries)

    subject = build_subject(today)
    weather = get_weather()
    plain_body, html_body = build_email_body(
    today,
    ai_summaries,
    india_summaries,
    key_takeaway,
    weather,
)

    if args.save_preview or args.dry_run:
        Path("email_preview.txt").write_text(plain_body, encoding="utf-8")
        Path("email_preview.html").write_text(html_body, encoding="utf-8")
        print("Preview saved to email_preview.txt and email_preview.html.")

    if args.dry_run:
        print("\n--- EMAIL SUBJECT ---")
        print(subject)
        print("\n--- EMAIL PREVIEW ---")
        print(plain_body[:3000])
        print("\nDry run complete. No email was sent.")
        return 0

    settings = _load_email_settings()
    send_email(settings, subject, plain_body, html_body)
    print(f"Email sent to {settings.to_email}.")
    return 0


def _load_email_settings() -> EmailSettings:
    gmail_address = os.getenv("GMAIL_ADDRESS", "").strip()
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip().replace(" ", "")
    to_email = os.getenv("TO_EMAIL", "").strip()
    sender_name = os.getenv("SENDER_NAME", "Daily News Bot").strip()

    missing = [
        name
        for name, value in {
            "GMAIL_ADDRESS": gmail_address,
            "GMAIL_APP_PASSWORD": gmail_app_password,
            "TO_EMAIL": to_email,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required .env values: {', '.join(missing)}")

    return EmailSettings(
        gmail_address=gmail_address,
        gmail_app_password=gmail_app_password,
        to_email=to_email,
        sender_name=sender_name,
    )


def _get_int_env(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    if not raw_value:
        return default
    try:
        return int(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a number, but got {raw_value!r}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
