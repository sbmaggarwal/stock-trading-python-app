import os
import json
import csv
from dotenv import load_dotenv
from fetch_tickers import fetch_tickers

# Load environment variables from a .env file (if present). Use override=True so
# a blank/empty environment variable will be replaced by the .env value.
load_dotenv(override=True)

# Read the API key from environment (default to empty string)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "")

# Strip optional surrounding quotes that may be present in some .env formats
if POLYGON_API_KEY.startswith('"') and POLYGON_API_KEY.endswith('"'):
    POLYGON_API_KEY = POLYGON_API_KEY[1:-1]
elif POLYGON_API_KEY.startswith("'") and POLYGON_API_KEY.endswith("'"):
    POLYGON_API_KEY = POLYGON_API_KEY[1:-1]

if not POLYGON_API_KEY:
    print("Error: POLYGON_API_KEY is not set or is empty after loading .env.\n"
          "1) Check your shell for an exported empty POLYGON_API_KEY that could block dotenv,\n"
          "2) Or set the key in .env without surrounding quotes, e.g. POLYGON_API_KEY=your_key\n"
          )
    raise SystemExit(1)

# Use params to build the request instead of manual string concatenation
base_url = "https://api.polygon.io/v3/reference/tickers"
params = {
    "market": "stocks",
    "active": "true",
    "order": "asc",
    "limit": "100",
    "sort": "ticker",
    "apiKey": POLYGON_API_KEY,
}

# Use the fetch_tickers module to get the response
response = fetch_tickers(POLYGON_API_KEY)
print(response.request.url, response)

# Parse JSON response and write results to CSV with same schema (flattened)
data = response.json()

if response.status_code != 200:
    # Print server error and exit
    print("Error fetching data:", response.status_code, data.get(
        'error') if isinstance(data, dict) else response.text)
    raise SystemExit(1)

results = data.get("results") if isinstance(data, dict) else None
if not results:
    print("No results found in response.")
    raise SystemExit(0)


def flatten(obj, parent_key='', sep='.'):
    """Flatten nested dicts into a single-level dict with dot-separated keys.

    Lists of primitives are joined with '|'. Other lists are JSON-encoded.
    """
    items = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(flatten(v, new_key, sep=sep))
    elif isinstance(obj, list):
        if all(isinstance(x, (str, int, float, bool, type(None))) for x in obj):
            items[parent_key] = '|'.join(
                '' if x is None else str(x) for x in obj)
        else:
            items[parent_key] = json.dumps(obj, ensure_ascii=False)
    else:
        items[parent_key] = obj
    return items


# Build flattened rows and header set
rows = []
headers = set()
for item in results:
    flat = flatten(item)
    rows.append(flat)
    headers.update(flat.keys())

headers = sorted(headers)
csv_path = os.path.join(os.getcwd(), 'tickers.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for r in rows:
        # Ensure all headers exist in row
        row_out = {h: r.get(h, '') for h in headers}
        writer.writerow(row_out)

print(f'Wrote {len(rows)} rows to {csv_path}')
