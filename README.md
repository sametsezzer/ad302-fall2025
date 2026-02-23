# Sites Project

A two-part data pipeline that collects contact phone numbers from 20 websites using the OpenAI API, then displays a business summary in a local web app.

---

## Project Structure

```
sites project/
├── sites.csv             # Input: 20 website URLs
├── generate_content.py   # Phase 1: data collection script
├── phones.csv            # Output: collected phone numbers
├── content.txt           # Output: business summary for first site
├── README.md
└── app/
    ├── package.json
    ├── server.js         # Express backend
    └── public/
        └── index.html    # Frontend UI
```

---

## Prerequisites

- Python 3.8+ with the `openai` package (`pip install openai`)
- Node.js 18+ and npm
- An OpenAI API key with access to `gpt-4o-search-preview`

---

## Setup

### 1. Set your OpenAI API key

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

**macOS / Linux:**
```bash
export OPENAI_API_KEY=your_api_key_here
```

---

## Phase 1 — Data Collection

Reads all 20 URLs from `sites.csv`, finds phone numbers in parallel via the OpenAI web search API, and researches the first site to generate a summary.

```bash
python generate_content.py
```

**Output files:**
- `phones.csv` — two columns: `url`, `phone`
- `content.txt` — 3–4 sentence summary of https://www.atelierboho.com.tr/

---

## Phase 2 — Web App

Serves a single-page UI showing the Atelier Boho summary with links to both sites.

```bash
cd app && npm install && node server.js
```

Then open **http://localhost:3000** in your browser.

The page displays:
- The summary loaded from `content.txt`
- **Visit Atelier Boho** → https://www.atelierboho.com.tr/
- **Visit Alight Apps** → https://www.alightapps.com/

---

## Notes

- `OPENAI_API_KEY` must be set before running `generate_content.py`
- The Express server reads `content.txt` from `../content.txt` relative to the `app/` folder — run `node server.js` from inside the `app/` directory
- Phone lookups run with 10 parallel threads to minimise total runtime
