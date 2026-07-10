"""Simple, free summarization helpers.

This project avoids paid AI APIs by default. The summaries are created from RSS
titles/descriptions using small text-cleaning rules that are easy to understand.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from news_fetcher import NewsItem


@dataclass(frozen=True)
class SummaryItem:
    title: str
    date: str
    summary: str
    why_it_matters: str
    source_link: str
    source_name: str
    image_url: str


def summarize_item(item: NewsItem) -> SummaryItem:
    summary = _simple_summary(item)
    why_it_matters = _why_it_matters(item)
    return SummaryItem(
        title=item.title,
        date=item.published.strftime("%Y-%m-%d"),
        summary=summary,
        why_it_matters=why_it_matters,
        source_link=item.link,
        source_name=item.source_name,
        image_url=item.image_url,
    )


def create_key_takeaway(ai_items: list[SummaryItem], india_items: list[SummaryItem]) -> str:
    ai_focus = _dominant_theme(" ".join(item.title for item in ai_items), "AI")
    india_focus = _dominant_theme(" ".join(item.title for item in india_items), "India")
    return (
        f"AI activity is centered on {ai_focus}, while India's major updates are focused on "
        f"{india_focus}. The useful habit today is to watch both technology shifts and policy/economy news together."
    )


def _simple_summary(item: NewsItem) -> str:
    source_text = item.summary_text or item.title
    sentences = _split_sentences(source_text)

    if not sentences:
        return f"This update reports that {item.title}. Read the source for the full details."

    clean_sentences = []
    for sentence in sentences[:3]:
        sentence = sentence.strip()
        if sentence and sentence not in clean_sentences:
            clean_sentences.append(sentence)

    summary = " ".join(clean_sentences)
    if len(summary) < 90 and item.title not in summary:
        summary = f"{item.title}. {summary}"

    return summary[:700].strip()


def _why_it_matters(item: NewsItem) -> str:
    text = f"{item.title} {item.summary_text}".lower()

    if item.category == "ai":
        if any(word in text for word in ("hallucination", "hallucinated", "fake citation", "fabricated")):
            return "It highlights why AI output still needs human checking, especially in serious or expert work."
        if any(word in text for word in ("regulation", "policy", "law", "safety")):
            return "It may affect how AI tools are governed, trusted, and used by companies or the public."
        if any(word in text for word in ("model", "openai", "gemini", "claude", "llm", "deepmind")):
            return "It may change what AI tools can do and what developers or businesses can build next."
        if any(word in text for word in ("chip", "nvidia", "semiconductor", "data center")):
            return "AI progress depends heavily on computing power, chips, and infrastructure."
        return "It helps track where global AI research, products, and adoption are moving."

    if any(word in text for word in ("rbi", "economy", "market", "inflation", "gdp")):
        return "It can affect jobs, prices, investments, and business decisions in India."
    if any(word in text for word in ("court", "law", "policy", "government", "ministry")):
        return "It may affect public policy, governance, or everyday rules for citizens."
    if any(word in text for word in ("weather", "monsoon", "flood", "heat")):
        return "Weather updates can affect travel, safety, farming, and local planning."
    return "It is part of the larger national picture and may affect people, policy, or the economy."


def _dominant_theme(text: str, fallback: str) -> str:
    lower_text = text.lower()
    themes = {
        "new models and product launches": ("model", "launch", "chatgpt", "gemini", "claude"),
        "policy and regulation": ("policy", "law", "regulation", "government", "court"),
        "business and markets": ("market", "stock", "company", "deal", "investment"),
        "public safety and weather": ("weather", "monsoon", "flood", "heat", "security"),
        "research and infrastructure": ("research", "chip", "data center", "nvidia", "infrastructure"),
    }
    best_theme = fallback
    best_score = 0
    for theme, keywords in themes.items():
        score = sum(1 for keyword in keywords if keyword in lower_text)
        if score > best_score:
            best_theme = theme
            best_score = score
    return best_theme


def _split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return []
    return re.split(r"(?<=[.!?])\s+", text)
