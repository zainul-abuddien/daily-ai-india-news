"""Fetch and rank news items from RSS feeds."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from config import AI_KEYWORDS, EXCLUDED_TITLE_KEYWORDS, INDIA_KEYWORDS, Category, FeedSource


@dataclass(frozen=True)
class NewsItem:
    title: str
    link: str
    published: datetime
    summary_text: str
    image_url: str
    source_name: str
    category: Category
    score: int


def fetch_top_items(
    feeds: Iterable[FeedSource],
    category: Category,
    limit: int = 5,
    max_age_hours: int = 48,
) -> list[NewsItem]:
    """Fetch, deduplicate, and rank the top news items for one category."""
    now = datetime.now(timezone.utc)
    oldest_allowed = now - timedelta(hours=max_age_hours)
    seen: set[str] = set()
    items: list[NewsItem] = []

    for feed in feeds:
        if feed.category != category:
            continue

        try:
            parsed_feed = _fetch_feed(feed.url)
        except Exception as exc:
            print(f"Warning: could not fetch {feed.name}: {exc}")
            continue

        for entry in parsed_feed.entries:
            title = _clean_text(entry.get("title", "Untitled"))
            link = entry.get("link", "").strip()
            published = _parse_date(entry)
            summary_text = _clean_text(
                entry.get("summary")
                or entry.get("description")
                or entry.get("subtitle")
                or ""
            )

            if not title or not link:
                continue
            if _is_excluded_title(title):
                continue
            if _is_placeholder_item(title, summary_text, link):
                continue

            key = _dedupe_key(title, link)
            if key in seen:
                continue
            seen.add(key)

            # Some feeds do not publish dates reliably. Keep undated items, but
            # rank them lower by assigning today's date only after age filtering.
            if published and published < oldest_allowed:
                continue
            published = published or now

            text_for_scoring = f"{title} {summary_text}".lower()
            keyword_score = _keyword_score(text_for_scoring, category)
            if category == "ai" and keyword_score == 0:
                continue

            age_hours = max(0, int((now - published).total_seconds() // 3600))
            recency_score = max(0, 48 - age_hours)
            score = feed.priority * 10 + keyword_score * 4 + recency_score

            items.append(
                NewsItem(
                    title=title,
                    link=link,
                    published=published,
                    summary_text=summary_text,
                    image_url=_extract_image(entry),
                    source_name=feed.name,
                    category=category,
                    score=score,
                )
            )

    ranked_items = sorted(items, key=lambda item: item.score, reverse=True)
    return _select_diverse_items(ranked_items, limit)


def _fetch_feed(url: str):
    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "daily-ai-india-news-bot/1.0 (+personal RSS reader)",
        },
    )
    response.raise_for_status()
    return feedparser.parse(response.content)


def _parse_date(entry) -> datetime | None:
    for field_name in ("published", "updated", "created"):
        value = entry.get(field_name)
        if not value:
            continue
        try:
            parsed = date_parser.parse(value)
        except (TypeError, ValueError):
            try:
                parsed = parsedate_to_datetime(value)
            except (TypeError, ValueError):
                continue
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    return None


def _clean_text(value: str) -> str:
    value = value or ""
    if "<" not in value and ">" not in value:
        text = value
    else:
        soup = BeautifulSoup(value, "html.parser")
        text = soup.get_text(" ", strip=True)
    return " ".join(text.split())


def _dedupe_key(title: str, link: str) -> str:
    simplified_title = "".join(ch.lower() for ch in title if ch.isalnum() or ch.isspace())
    return f"{simplified_title[:90]}::{link.split('?')[0]}"


def _is_placeholder_item(title: str, summary_text: str, link: str) -> bool:
    combined = f"{title} {summary_text} {link}".lower()
    placeholder_markers = (
        "this feed is not available",
        "for the latest headlines, visit google news",
        "enable javascript",
        "access denied",
    )
    return any(marker in combined for marker in placeholder_markers)


def _is_excluded_title(title: str) -> bool:
    lower_title = title.lower()
    return any(keyword in lower_title for keyword in EXCLUDED_TITLE_KEYWORDS)


def _keyword_score(text: str, category: Category) -> int:
    keywords = AI_KEYWORDS if category == "ai" else INDIA_KEYWORDS
    return sum(1 for keyword in keywords if keyword in text)


def _select_diverse_items(items: list[NewsItem], limit: int, per_source_limit: int = 2) -> list[NewsItem]:
    selected: list[NewsItem] = []
    selected_links: set[str] = set()
    source_counts: dict[str, int] = {}

    for item in items:
        if len(selected) >= limit:
            break
        if source_counts.get(item.source_name, 0) >= per_source_limit:
            continue
        selected.append(item)
        selected_links.add(item.link)
        source_counts[item.source_name] = source_counts.get(item.source_name, 0) + 1

    if len(selected) < limit:
        for item in items:
            if len(selected) >= limit:
                break
            if item.link in selected_links:
                continue
            selected.append(item)
            selected_links.add(item.link)

    return selected
def _extract_image(entry) -> str:
    # media:thumbnail
    media = entry.get("media_thumbnail")
    if media and len(media):
        return media[0].get("url", "")

    # media:content
    media = entry.get("media_content")
    if media and len(media):
        return media[0].get("url", "")

    # enclosure
    if "links" in entry:
        for link in entry.links:
            if getattr(link, "type", "").startswith("image"):
                return getattr(link, "href", "")

    return ""
