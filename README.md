# Discord Bot Setup

Quick steps to get the bot running locally.

Prerequisites:
- Python 3.8+
- A Discord application and bot token (from the Discord Developer Portal)

1) Install dependencies

```
pip install -r requirements.txt
```

2) Create your `.env` file

Copy `.env.example` to `.env` and paste your bot token:

```
DISCORD_TOKEN=YOUR_REAL_TOKEN_HERE
```

3) Enable intents

If your bot needs message content access (it does for the `!ping` command), enable the "Message Content Intent" in the Developer Portal under your Bot -> Privileged Gateway Intents.

4) Run the bot

```
python bot.py
```

5) Invite the bot to your server

Generate an invite URL in the Developer Portal (OAuth2 -> URL Generator). Scopes: `bot` (and `applications.commands` if you plan to add slash commands). Then select the permissions your bot requires and open the generated URL to invite it.

Notes:
- Keep your token secret. Do not commit `.env` to source control.
- If you want the bot to run continuously, consider hosting options (Heroku, Railway, VPS, or a Docker container).

## New command: `!build`

Once the bot is running, use:

```
!build hiyuki
```

This will return a styled build guide for Hiyuki in Discord. Additional characters can be added later by adding new entries in `data/characterbuilds.json`.
