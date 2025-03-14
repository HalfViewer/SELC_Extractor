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

### Basic Usage

Run the script with a URL to scrape:

```bash
python main.py <url>
```

Where `<url>` is the full URL of the SELC webpage you want to scrape.

### Example:

```bash
python main.py https://example-selc-site.com/page-to-scrape
```

This will scrape the page and output the JSON data to the console.

### Saving Output to a File

To save the results to a JSON file, use the `-o` or `--output` parameter:

```bash
python main.py <url> -o <output_file.json>
```

### Example:

```bash
python main.py https://example-selc-site.com/page-to-scrape -o results.json
```

This will scrape the page and save the output to `results.json` in the current directory.

## Parameters

| Parameter | Description |
|-----------|-------------|
| url | Required. The URL of the SELC webpage to scrape |
| -o, --output | Optional. Output file path to save JSON results |

## Expected Output

The script will:
1. Launch a headless browser
2. Navigate to the specified URL
3. Extract data from tables with the specified XPaths
4. Output the data in JSON format (to console or file)
5. Close the browser

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

## Troubleshooting

If you encounter any issues:
- Make sure the URL is correct and accessible
- Check that you have the correct permissions to access the page
- Ensure all dependencies are properly installed
- If tables aren't being found, the XPaths might need adjustment
