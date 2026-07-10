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
) -> tuple[str, str]:
    plain = _build_plain_text(date_label, ai_items, india_items, key_takeaway)
    html_body = _build_html(date_label, ai_items, india_items, key_takeaway)
    return plain, html_body


def send_email(settings: EmailSettings, subject: str, plain_body: str, html_body: str) -> None:
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
) -> str:
    lines = [
        "Good morning,",
        "",
        f"Here is your Daily AI + India News Update for {date_label}.",
        "",
        "Section 1: Top 5 AI Updates in the World",
        "",
    ]
    lines.extend(_plain_items(ai_items))
    lines.extend(["", "Section 2: Top 5 India News Updates", ""])
    lines.extend(_plain_items(india_items))
    lines.extend(["", "Today's key takeaway", key_takeaway, "", "Have a good day!"])
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

def _html_section(title, items):

    blocks=[f'<div class="section"><div class="section-title">{title}</div>']

    for item in items:

        blocks.append(f"""

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

""")

    blocks.append("</div>")

    return "\n".join(blocks)


def _html_section(title: str, items: list[SummaryItem]) -> str:
    blocks = [f"<h2>{html.escape(title)}</h2>"]
    for index, item in enumerate(items, start=1):
        blocks.append(
            f"""
    <div style="margin-bottom: 22px;">
      <h3 style="margin-bottom: 6px;">{index}. {html.escape(item.title)}</h3>
      <p style="margin: 0 0 6px;"><strong>Date:</strong> {html.escape(item.date)}</p>
      <p style="margin: 0 0 6px;"><strong>Summary:</strong> {html.escape(item.summary)}</p>
      <p style="margin: 0 0 6px;"><strong>Why it matters:</strong> {html.escape(item.why_it_matters)}</p>
      <p style="margin: 0;"><strong>Source:</strong> {html.escape(item.source_name)} -
        <a href="{html.escape(item.source_link)}">Read more</a>
      </p>
    </div>"""
        )
    return "\n".join(blocks)
