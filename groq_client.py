from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_summary(news_text: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional daily news editor. "
                    "Write concise newsletter summaries."
                )
            },
            {
                "role": "user",
                "content": f"""
Summarize this news in 3-4 clear sentences.

Rules:
- Write only the summary.
- Do not explain why it matters.
- Do not write "This news matters because".
- Do not add headings.
- Keep it factual and easy to understand.
- Remove unnecessary details.

News:
{news_text}
"""
            }
        ],
        temperature=0.4,
        max_tokens=250
    )

    return response.choices[0].message.content.strip()