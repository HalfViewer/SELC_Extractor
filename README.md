# SELC Web Scraper

A Python script to extract table data from SELC webpages using Playwright.

## Features

- Uses Playwright for browser automation to handle JavaScript-rendered content
- Extracts data from tables with specific XPaths
- Captures signoff names, statuses, dates, and comments
- Outputs data in JSON format

## Requirements

- Python 3.7+
- Required packages listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:

```bash
python -m playwright install
```

## Usage

Run the script with a URL to scrape:

```bash
python main.py https://example-selc-site.com/page-to-scrape
```

To save the output to a file:

```bash
python main.py https://example-selc-site.com/page-to-scrape -o output.json
```

## Output Format

The script outputs data in JSON format with the following structure:

```json
{
  "main_table_found": true,
  "status_tables": [
    {
      "table_index": 2,
      "entries": [
        {
          "signoff_name": "...",
          "status": "...",
          "date": "...",
          "comment": "..."
        },
        ...
      ]
    },
    ...
  ],
  "detail_table_5": {
    "table_index": 5,
    "entries": [...]
  }
}
``` 