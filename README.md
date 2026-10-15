# Indian market morning brief

A daily 9:00 a.m. IST target start on GitHub-hosted runners. No laptop or Codex session is needed after deployment. GitHub scheduling may be delayed or a run dropped during high load.

## What the free version includes

Recent dated Economic Times and Moneycontrol market headlines, Gemini summary, source links, and a plain headline fallback if Gemini fails. This is a news digest, not a live price terminal: index closes, GIFT Nifty, FII/DII flows, full article contents and exchange holiday status are not verified. The original local Codex report has broader web research; this free version has narrower coverage. No search grounding or paid data service is used.

Gemini defaults to `gemini-3.5-flash-lite`. Confirm your project is on Google's Free tier; the script cannot enforce your account's billing settings. Free quota and model availability can change. Change repository variable `GEMINI_MODEL` if necessary. GitHub Actions usage shares your account's included allowance. Keep paid usage disabled if you require zero spend.

## Set up

1. Create a private GitHub repository named `indian-market-agent`.
2. Upload `market_agent.py`, `tests/test_agent.py` and `.github/workflows/market-report.yml`, preserving the folders. Also upload this README and `.gitignore`. Commit them to the repository's default branch. The Windows `send-telegram.ps1` file is not needed.
3. In the repository open **Settings → Secrets and variables → Actions → New repository secret**. Add:

| Secret name | Value |
| --- | --- |
| `GEMINI_API_KEY` | Your Google AI Studio key |
| `TELEGRAM_BOT_TOKEN` | Token from BotFather, not the bot username |
| `TELEGRAM_CHAT_ID` | Your numeric Telegram chat ID (provided in the setup chat) |

Never paste credentials into code, repository files, issues, or chat. Your Windows-encrypted token file cannot be decrypted on GitHub: enter the original BotFather token directly as a GitHub secret.

4. Open **Actions → Indian market morning report → Run workflow**. Enable `test_only` for a Telegram-only test. After receiving it, run again with `test_only` unchecked for a complete report and check that the AI summary appears (rather than the fallback).
5. After cloud delivery works, disable the existing local Codex automation to avoid duplicate reports. Until then, the local schedule remains active.

The schedule runs every day, including weekends. On holidays it may still send recent headlines. It does not determine an official holiday calendar. Reports include retrieval failures and timestamps; old or undated headlines are excluded. If Telegram fails, the Actions run fails. Enable GitHub Actions failure notifications in your account. A partly delivered report can be duplicated if you manually rerun it.

## Local verification

Python 3.12, no additional packages:

```sh
python -m unittest discover -s tests -v
```

The tests use mocked data. End-to-end Gemini and GitHub cloud delivery require your privately configured secrets.
