# Kalshi Markets Dashboard

Live dashboard for browsing all open [Kalshi](https://kalshi.com) prediction markets.

## Features

- **Live data** — fetches directly from the Kalshi public API (no auth required)
- **4,600+ events** across 15 categories (Sports, Politics, Crypto, Economics, etc.)
- **Category filtering** — sidebar to drill into specific market categories
- **Full-text search** — filter by event title or ticker
- **Expandable events** — click any event to see individual markets with Yes/No bid prices and volume
- **Progressive loading** — first page renders in ~300ms, rest streams in background
- **localStorage cache** — subsequent page loads are instant (5-min TTL)
- **Progress bar** — visual loading indicator
- **Dark theme** — GitHub-dark aesthetic
- **Mobile responsive**

## How It Works

Single self-contained HTML file. No build step, no dependencies, no server required.

Opens the [Kalshi public API](https://docs.kalshi.com) (`api.elections.kalshi.com`) directly from the browser with CORS proxy fallback for local file access.

## Kalshi Tickers

Kalshi uses **proprietary tickers** (no Bloomberg, Reuters, or standard financial identifiers):

| Component | Example | Meaning |
|---|---|---|
| Prefix | `KX` | Kalshi exchange marker |
| Series | `BTCMAXY` | Mnemonic topic code |
| Suffix | `-26DEC31` | Date/variant identifier |

## Deploy

Host anywhere that serves static files:

- **GitHub Pages** — push this repo, enable Pages in Settings
- **Netlify** — drag `index.html` onto [app.netlify.com/drop](https://app.netlify.com/drop)
- **Local** — `python3 -m http.server 8080` then open `localhost:8080`

## API Reference

- Base URL: `https://api.elections.kalshi.com/trade-api/v2`
- Docs: [docs.kalshi.com](https://docs.kalshi.com)
- No authentication needed for market data endpoints
