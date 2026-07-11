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
                    "Create concise, accurate summaries for a newsletter."
                )
            },
            {
                "role": "user",
                "content": f"""
Summarize this news in 3-5 sentences.

Also explain why this news matters.

News:
{news_text}
"""
            }
        ],
        temperature=0.4,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()