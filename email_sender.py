"""Render and send the daily email through Gmail SMTP."""

from __future__ import annotations

from pathlib import Path

import html
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage

from summarizer import SummaryItem


@dataclass(frozen=True)
class EmailSettings:
    gmail_address: str
    gmail_app_password: str
    to_email: str
    sender_name: str = "Daily News Bot"


def build_subject(date_label: str) -> str:
    return f"Daily AI + India News Update - {date_label}"


def build_email_body(
    date_label: str,
    ai_items: list[SummaryItem],
    india_items: list[SummaryItem],
    key_takeaway: str,
    weather: dict,
) -> tuple[str, str]:

    plain = _build_plain_text(
        date_label,
        ai_items,
        india_items,
        key_takeaway,
        weather,
    )

    html_body = _build_html(
        date_label,
        ai_items,
        india_items,
        key_takeaway,
        weather,
    )

    return plain, html_body


def send_email(
    settings: EmailSettings,
    subject: str,
    plain_body: str,
    html_body: str,
) -> None:

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{settings.sender_name} <{settings.gmail_address}>"
    message["To"] = settings.to_email

    message.set_content(plain_body)
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(settings.gmail_address, settings.gmail_app_password)
        smtp.send_message(message)


def _build_plain_text(
    date_label: str,
    ai_items: list[SummaryItem],
    india_items: list[SummaryItem],
    key_takeaway: str,
    weather: dict,
) -> str:

    lines = [
        "Good morning,",
        "",
        f"Here is your Daily AI + India News Update for {date_label}.",
        "",
        "🌦️ Today's Weather",
        f"Temperature: {weather['temperature']}",
        f"Humidity: {weather['humidity']}",
        f"Condition: {weather['condition']}",
        "",
        "Section 1: Top 5 AI Updates in the World",
        "",
    ]

    lines.extend(_plain_items(ai_items))

    lines.extend(
        [
            "",
            "Section 2: Top 5 India News Updates",
            "",
        ]
    )

    lines.extend(_plain_items(india_items))

    lines.extend(
        [
            "",
            "Today's key takeaway",
            key_takeaway,
            "",
            "Have a good day!",
        ]
    )

    return "\n".join(lines)


def _plain_items(items: list[SummaryItem]) -> list[str]:

    lines: list[str] = []

    for index, item in enumerate(items, start=1):

        lines.extend(
            [
                f"{index}. {item.title}",
                f"Date: {item.date}",
                f"Summary: {item.summary}",
                f"Why it matters: {item.why_it_matters}",
                f"Source: {item.source_name} - {item.source_link}",
                "",
            ]
        )

    return lines


def load_template():

    template = Path("templates/email.html")

    return template.read_text(encoding="utf-8")


def _build_html(
    date_label: str,
    ai_items: list[SummaryItem],
    india_items: list[SummaryItem],
    key_takeaway: str,
    weather: dict,
) -> str:

    template = load_template()

    header = f"""
<div class="header">
<h1>📰 Daily AI + India News</h1>
<div class="date">{html.escape(date_label)}</div>
</div>
"""

    weather_html = f"""
<div class="section">

<div class="section-title">🌦️ Today's Weather</div>

<div class="card">

<h2>Gangavathi Weather</h2>

<p><b>Temperature:</b> {html.escape(weather["temperature"])}</p>

<p><b>Humidity:</b> {html.escape(weather["humidity"])}</p>

<p><b>Condition:</b> {html.escape(weather["condition"])}</p>

</div>

</div>
"""

    ai_html = _html_section("🤖 Top AI News", ai_items)

    india_html = _html_section("🇮🇳 Top India News", india_items)


    footer = """
<div class="footer">
Made with ❤️ using Python + GitHub Actions
</div>
"""


    template = template.replace("{{HEADER}}", header)

    template = template.replace(
        "{{AI_NEWS}}",
        weather_html + ai_html,
    )

    template = template.replace(
        "{{INDIA_NEWS}}",
        india_html,
    )

    template = template.replace(
        "{{FOOTER}}",
        footer,
    )


    return template


def _html_section(title, items):

    blocks = [
        f'<div class="section"><div class="section-title">{title}</div>'
    ]


    for item in items:

        blocks.append(
            f"""
<div class="card">

<h2>{html.escape(item.title)}</h2>

<p><b>Date:</b> {item.date}</p>

<p class="summary">
{html.escape(item.summary)}
</p>

<p>
<b>Why it matters:</b>
{html.escape(item.why_it_matters)}
</p>

<a class="button"
href="{item.source_link}">
Read More →
</a>

</div>
"""
        )


    blocks.append("</div>")


    return "\n".join(blocks)