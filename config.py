"""Configuration for the Daily AI + India News email project."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Category = Literal["ai", "india"]


@dataclass(frozen=True)
class FeedSource:
    name: str
    url: str
    category: Category
    priority: int = 1


AI_KEYWORDS = (
    "ai",
    "artificial intelligence",
    "openai",
    "chatgpt",
    "gpt",
    "gemini",
    "claude",
    "anthropic",
    "deepmind",
    "machine learning",
    "large language model",
    "llm",
    "model",
    "robotics",
    "automation",
    "agent",
    "agents",
    "generative",
    "neural",
    "nvidia",
    "semiconductor",
)

INDIA_KEYWORDS = (
    "india",
    "indian",
    "new delhi",
    "parliament",
    "supreme court",
    "rbi",
    "economy",
    "election",
    "policy",
    "government",
    "ministry",
    "security",
    "weather",
    "monsoon",
    "markets",
)

EXCLUDED_TITLE_KEYWORDS = (
    "quote of the day",
    "horoscope",
    "lottery",
    "shopping",
    "coupon",
    "viral video",
)


FEEDS: tuple[FeedSource, ...] = (
    FeedSource(
        name="MIT News - Artificial Intelligence",
        url="https://news.mit.edu/rss/topic/artificial-intelligence2",
        category="ai",
        priority=5,
    ),
    FeedSource(
        name="TechCrunch - AI",
        url="https://techcrunch.com/category/artificial-intelligence/feed/",
        category="ai",
        priority=4,
    ),
    FeedSource(
        name="VentureBeat - AI",
        url="https://venturebeat.com/category/ai/feed/",
        category="ai",
        priority=3,
    ),
    FeedSource(
        name="Ars Technica - AI",
        url="https://arstechnica.com/ai/feed/",
        category="ai",
        priority=4,
    ),
    FeedSource(
        name="The Decoder",
        url="https://the-decoder.com/feed/",
        category="ai",
        priority=3,
    ),
    FeedSource(
        name="AI News",
        url="https://www.artificialintelligence-news.com/feed/",
        category="ai",
        priority=3,
    ),
    FeedSource(
        name="Google News - AI",
        url=(
            "https://news.google.com/rss/search?"
            "q=artificial%20intelligence%20OR%20OpenAI%20OR%20ChatGPT%20OR%20Gemini%20OR%20Claude%20when:2d"
            "&hl=en-US&gl=US&ceid=US:en"
        ),
        category="ai",
        priority=2,
    ),
    FeedSource(
        name="Google News - India Top Stories",
        url="https://news.google.com/rss/headlines/section/geo/IN?hl=en-IN&gl=IN&ceid=IN:en",
        category="india",
        priority=5,
    ),
    FeedSource(
        name="The Hindu - National",
        url="https://www.thehindu.com/news/national/feeder/default.rss",
        category="india",
        priority=4,
    ),
    FeedSource(
        name="Indian Express - India",
        url="https://indianexpress.com/section/india/feed/",
        category="india",
        priority=4,
    ),
    FeedSource(
        name="Mint - News",
        url="https://www.livemint.com/rss/news",
        category="india",
        priority=3,
    ),
    FeedSource(
        name="NDTV - India",
        url="https://feeds.feedburner.com/ndtvnews-india-news",
        category="india",
        priority=3,
    ),
)
