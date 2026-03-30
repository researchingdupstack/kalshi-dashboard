#!/usr/bin/env python3
"""Fetch all available Kalshi markets and generate a static HTML dashboard.

Uses the events endpoint with nested markets to avoid paging through
100k+ auto-generated combo/parlay markets.
"""

import json
import urllib.request
import urllib.parse
import time
from datetime import datetime, timezone

API_BASE = "https://api.elections.kalshi.com/trade-api/v2"
EVENTS_ENDPOINT = f"{API_BASE}/events"
LIMIT = 200
PAGE_DELAY = 1.0
MAX_RETRIES = 5


def fetch_with_retry(url, retries=MAX_RETRIES):
    """Fetch a URL with retry on 429 rate limits."""
    for attempt in range(retries):
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                retry_after = int(e.headers.get("Retry-After", "5"))
                wait = max(retry_after, 2 ** (attempt + 1))
                print(f"429, waiting {wait}s... ", end="", flush=True)
                time.sleep(wait)
            else:
                raise
    return None


def fetch_events_with_markets():
    """Fetch all open events with nested markets in one pass."""
    print("Fetching events with nested markets...")
    events = []
    all_markets = []
    cursor = None
    page = 0

    while True:
        page += 1
        query = {
            "status": "open",
            "limit": str(LIMIT),
            "with_nested_markets": "true",
        }
        if cursor:
            query["cursor"] = cursor

        url = f"{EVENTS_ENDPOINT}?{urllib.parse.urlencode(query)}"
        print(f"  Page {page}... ", end="", flush=True)

        data = fetch_with_retry(url)
        batch = data.get("events", [])

        market_count = 0
        for event in batch:
            markets = event.pop("markets", [])
            # Only keep open/active markets
            open_markets = [m for m in markets if m.get("status") in ("open", "active")]
            market_count += len(open_markets)
            for m in open_markets:
                m["_category"] = event.get("category", "Other")
                m["_event_title"] = event.get("title", "")
            all_markets.extend(open_markets)
            events.append(event)

        print(f"{len(batch)} events, {market_count} markets (totals: {len(events)} events, {len(all_markets)} markets)")

        cursor = data.get("cursor")
        if not cursor or not batch:
            break
        time.sleep(PAGE_DELAY)

    return events, all_markets


def process_markets(markets):
    """Process raw market data into compact dashboard records."""
    processed = []
    for m in markets:
        last_price = m.get("last_price_dollars", "0.0000")
        yes_bid = m.get("yes_bid_dollars", "0.0000")
        yes_ask = m.get("yes_ask_dollars", "0.0000")
        volume_24h = float(m.get("volume_24h_fp", "0") or "0")
        open_interest = float(m.get("open_interest_fp", "0") or "0")

        try:
            price = float(last_price)
            if price == 0:
                bid, ask = float(yes_bid), float(yes_ask)
                if bid > 0 or ask > 0:
                    price = (bid + ask) / 2
        except (ValueError, TypeError):
            price = 0

        close_time = m.get("close_time", "")
        try:
            ct = datetime.fromisoformat(close_time.replace("Z", "+00:00"))
            close_display = ct.strftime("%b %d, %Y %H:%M UTC")
            close_sort = close_time
        except Exception:
            close_display = close_time
            close_sort = ""

        processed.append({
            "t": m.get("ticker", ""),
            "n": m.get("title", ""),
            "e": m.get("_event_title", ""),
            "c": m.get("_category", "Other"),
            "p": round(price * 100, 1),
            "v": round(volume_24h, 2),
            "oi": round(open_interest, 2),
            "ct": close_display,
            "cs": close_sort,
        })

    return processed


def main():
    print("=== Kalshi Markets Dashboard Generator ===")
    print(f"Started at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}\n")

    events, markets = fetch_events_with_markets()
    print(f"\n  → {len(events):,} events, {len(markets):,} markets\n")

    generated_at = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")

    print("Processing...")
    processed = process_markets(markets)
    processed.sort(key=lambda m: -m["v"])

    data = {
        "generated_at": generated_at,
        "total_markets": len(processed),
        "categories": sorted(set(m["c"] for m in processed)),
        "markets": processed,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))

    size_kb = len(json.dumps(data, separators=(",", ":"))) / 1024
    print(f"\n✓ data.json: {size_kb:.0f} KB | {len(processed):,} markets | {len(data['categories'])} categories")
    print(f"Finished at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")


if __name__ == "__main__":
    main()
