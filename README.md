# Daily AI + India News Email Automation

This beginner-friendly Python project sends you a daily Gmail email with:

- Top 5 AI updates in the world
- Top 5 important India news updates
- Simple summaries
- Why each item matters
- Source links
- One short daily takeaway

It uses free RSS feeds by default, so you do not need a paid news API.

## Folder Structure

```text
daily-ai-india-news/
  .env.example
  .gitignore
  config.py
  email_sender.py
  main.py
  news_fetcher.py
  requirements.txt
  summarizer.py
  docs/
    scheduling.md
  .github/
    workflows/
      daily-news.yml
```

## How It Works

1. `news_fetcher.py` reads RSS feeds.
2. It keeps recent items, removes duplicates, and ranks them.
3. `summarizer.py` creates simple summaries from the RSS title/description.
4. `email_sender.py` formats the email and sends it with Gmail SMTP.
5. `main.py` connects everything and gives you a dry-run test mode.

## Reliable News Sources Used

AI news:

- MIT News - Artificial Intelligence RSS
- TechCrunch AI RSS
- VentureBeat AI RSS
- Ars Technica AI RSS
- The Decoder RSS
- AI News RSS
- Google News AI search RSS

India news:

- Google News India top stories RSS
- The Hindu National RSS
- Indian Express India RSS
- Mint News RSS
- NDTV India RSS

RSS feeds are beginner-friendly because most do not need API keys. If a feed stops working, replace its URL in `config.py`.

The Press Information Bureau also has an official RSS page, but it may reject automated requests from some environments. You can add it back in `config.py` if it works on your machine.

## Optional News APIs

You do not need these for the included code, but they are useful upgrades later:

- NewsAPI: easy REST API, free developer use, requires an API key from `newsapi.org`.
- GDELT: free global news database/API, powerful but more technical.

For a beginner, start with RSS. It is simpler and avoids API-key setup.

## Setup

### 1. Install Python

Install Python 3.11 or newer from:

```text
https://www.python.org/downloads/
```

During install, enable **Add Python to PATH**.

### 2. Create a virtual environment

Open PowerShell in this folder:

```powershell
cd C:\Users\zainu\Downloads\latest\daily-ai-india-news
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again.

### 3. Install libraries

```powershell
pip install -r requirements.txt
```

Required libraries:

- `feedparser` for RSS feeds
- `requests` for downloading feeds
- `beautifulsoup4` for cleaning HTML snippets
- `python-dotenv` for `.env`
- `python-dateutil` for flexible date parsing

### 4. Create your `.env`

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Fill it like this:

```env
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
TO_EMAIL=your_email@gmail.com
SENDER_NAME=Daily News Bot
MAX_NEWS_AGE_HOURS=48
TIMEZONE=Asia/Kolkata
```

Do not put your normal Gmail password here. Use a Gmail App Password.

## Gmail App Password Safety

To use Gmail SMTP safely:

1. Turn on 2-Step Verification in your Google Account.
2. Open Google App Passwords.
3. Create an app password for this project.
4. Put that 16-character app password in `.env`.

Never upload `.env` to GitHub. This project includes `.gitignore` so `.env` is ignored.

Safe to upload:

- `.env.example`
- Python code
- `requirements.txt`
- README files

Not safe to upload:

- `.env`
- Gmail App Password
- Any private API keys

## Test Mode

Run this before sending any real email:

```powershell
python main.py --dry-run
```

This fetches news and creates:

- `email_preview.txt`
- `email_preview.html`

No email is sent in dry-run mode.

## Send a Real Email

After dry-run looks good:

```powershell
python main.py --send
```

## Email Format

Subject:

```text
Daily AI + India News Update - [Date]
```

Body:

- Greeting
- Section 1: Top 5 AI Updates in the World
- Section 2: Top 5 India News Updates
- Each item includes title, date, summary, why it matters, and source link
- Today's key takeaway

## Add or Change RSS Feeds

Open `config.py` and add another `FeedSource`.

Example:

```python
FeedSource(
    name="Example News",
    url="https://example.com/rss",
    category="ai",
    priority=3,
)
```

Use `category="ai"` for AI news and `category="india"` for India news.

Higher `priority` means the source gets ranked slightly higher.

## Scheduling Recommendation

The easiest beginner option is **Windows Task Scheduler** if your laptop is on in the morning.

If you want the email to run even when your laptop is off, use **GitHub Actions** with repository secrets.

See `docs/scheduling.md` for step-by-step scheduling options.

## Common Errors and Fixes

### `python is not recognized`

Python is not installed or not added to PATH. Install Python again and enable **Add Python to PATH**.

### Gmail says username or password is wrong

Use a Gmail App Password, not your normal Gmail password. Also make sure 2-Step Verification is enabled.

### Not enough news items were found

Increase this in `.env`:

```env
MAX_NEWS_AGE_HOURS=72
```

Or add more feeds in `config.py`.

### A feed stops working

RSS feeds sometimes move. Replace the URL in `config.py` with a working RSS feed.

### GitHub Actions did not send email

Check:

- Secrets are named exactly `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`, and `TO_EMAIL`
- The app password has no spaces
- The workflow is enabled
- The repository has Actions enabled

## Final Setup Checklist

1. Install Python 3.11+.
2. Open this project folder in PowerShell.
3. Create and activate `.venv`.
4. Run `pip install -r requirements.txt`.
5. Copy `.env.example` to `.env`.
6. Add Gmail address, Gmail App Password, and recipient email.
7. Run `python main.py --dry-run`.
8. Open `email_preview.html` and check the output.
9. Run `python main.py --send`.
10. Schedule it with Windows Task Scheduler or GitHub Actions.
