# Kalshi Markets Dashboard

Live, publicly viewable dashboard of all available [Kalshi](https://kalshi.com) prediction markets.

**🔗 [View Dashboard](https://researchingdupstack.github.io/kalshi-dashboard/)**

## Features

- 📊 All active Kalshi markets in one view
- 🔍 Search by market name, event, ticker, or category
- 🏷️ Filter by category (Politics, Economics, Sports, Weather, etc.)
- 📈 Sort by volume, price, title, or closing time
- 🔄 Auto-updates every hour via GitHub Actions
- 📱 Responsive — works on mobile

## How It Works

1. A Python script fetches all active markets from the [Kalshi public API](https://docs.kalshi.com)
2. It generates a self-contained static HTML dashboard
3. GitHub Actions runs this every hour and deploys to GitHub Pages

No API key required — uses Kalshi's public market data endpoints.

## Run Locally

```bash
python fetch_markets.py
open index.html
```

## Data Source

All data comes from the Kalshi Exchange public API. This is not financial advice. Kalshi is a CFTC-regulated exchange.

## License

MIT
