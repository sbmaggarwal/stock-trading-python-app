## stock-trading-python-app

Small utility to fetch tickers from the Polygon REST API and write the results to a CSV.

What this repo contains
- `script.py` — entrypoint: loads environment, calls the fetcher, flattens the JSON response and writes `tickers.csv`.
- `fetch_tickers.py` — small module that encapsulates the HTTP request to Polygon (returns a `requests.Response`).
- `.env` — (not committed) place your `POLYGON_API_KEY` here. Example: `POLYGON_API_KEY=your_key`.
- `.gitignore` — updated to ignore `tickers.csv`, virtualenv folders (including `pythonenv/`), caches and IDE folders.

Quick start

1. Create a virtual environment and install dependencies (if not already done):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Add your Polygon API key to a `.env` file in the project root. Do NOT commit this file.

Recommended format (no surrounding quotes):

```text
POLYGON_API_KEY=your_actual_api_key_here
```

Note: the code strips surrounding single or double quotes if present, and `load_dotenv(override=True)` is used so an empty environment variable will be replaced by the `.env` value.

Run the script

```bash
python3 script.py
```

This will create `tickers.csv` in the repository root. The CSV columns are derived from the API response schema: nested fields are flattened into dot-separated column names. Simple lists are joined with `|` and complex lists are JSON-encoded.

Why files were split
- `fetch_tickers.py` isolates network logic so it can be reused, tested, or replaced without touching CSV/IO code in `script.py`.

Notes and next steps
- The CSV writer collects headers from all result rows to ensure a consistent schema. If you want a specific column order or a smaller set of columns, update `script.py` to specify `fieldnames`.
- Consider passing the API key via environment variables in CI rather than a `.env` file for production.
- I can add a small unit test for `fetch_tickers` (mocking requests) if you want.

If you want changes (different CSV layout, pagination handling, or returning JSON from the fetcher), tell me which direction and I will implement it.
