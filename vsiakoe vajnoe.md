## ZZZ-style Pulling Simulator (Telegram WebApp + FastAPI)

A minimal FastAPI backend serving a Telegram WebApp for a Zenless-like gacha (pull) simulator. Includes a Telegram bot that sends a button to open the WebApp.

### Features
- WebApp UI with Pull 1 / Pull 10
- Simple pity system (4★ at 10, 5★ at 90) with demo rates
- FastAPI `/api/pull` endpoint
- Telegram bot `/start` opens the WebApp inside Telegram

### Setup
1. Create a bot with BotFather and get your token.
2. Create a virtual environment and install deps.

```powershell
py -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Configure environment variables. Create `.env` with:

```env
BOT_TOKEN=123456789:YOUR_BOT_TOKEN
WEBAPP_URL=http://localhost:8000/
```

### Run locally
1. Start the FastAPI server (serves the WebApp on `/`):

```powershell
python .\main.py
```

2. In another terminal, run the Telegram bot:

```powershell
python .\bot.py
```

3. In Telegram, open your bot and send `/start`, then tap "Open Pull Simulator".

### Deploying
- Host the FastAPI app on a public URL (e.g., Render, Railway, Fly.io, or a VPS). Set `WEBAPP_URL` in your bot environment to that public URL.
- Optionally use a webhook instead of polling for production.

### Customize
- Edit pools and rates in `utils/gacha.py`.
- Modify UI in `webapp/`.

