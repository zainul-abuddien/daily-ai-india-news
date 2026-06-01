# Scheduling Options

This project can run anywhere that can run Python and access Gmail SMTP.

## Easiest beginner option: Windows Task Scheduler

Use this if your laptop is usually turned on in the morning.

1. Open **Task Scheduler**.
2. Choose **Create Basic Task**.
3. Name it `Daily AI India News Email`.
4. Trigger: **Daily**.
5. Time: choose your morning time, for example `08:00`.
6. Action: **Start a program**.
7. Program/script: path to your Python executable, for example:

   ```text
   C:\Users\zainu\Downloads\latest\daily-ai-india-news\.venv\Scripts\python.exe
   ```

8. Add arguments:

   ```text
   main.py --send
   ```

9. Start in:

   ```text
   C:\Users\zainu\Downloads\latest\daily-ai-india-news
   ```

## GitHub Actions option

Use this if you want the job to run even when your laptop is off.

Important: put secrets in **GitHub repository secrets**, not in `.env`.

Required secrets:

- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `TO_EMAIL`

The included workflow is in `.github/workflows/daily-news.yml`.

## Cloud/free hosting option

Good beginner-friendly choices:

- PythonAnywhere scheduled tasks
- Render cron jobs
- Railway cron jobs

Free tiers can change, so check the current limits before relying on them. The setup idea is the same everywhere:

1. Upload the project.
2. Add environment variables in the hosting dashboard.
3. Set the command to:

   ```bash
   python main.py --send
   ```

4. Schedule it for your morning time.
