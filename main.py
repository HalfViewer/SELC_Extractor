#!/usr/bin/env python3
import json
import argparse
import sys
import asyncio
from playwright.async_api import async_playwright

async def scrape_selc_webpage(url):
    try:
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Navigate to the URL
            await page.goto(url, wait_until='networkidle')
            
            # Initialize results dictionary
            results = {"status_tables": []}
            
            # Check for main table
            main_table = await page.query_selector('/html/body/form/table[2]/tbody/tr/td/table[2]')
            if main_table:
                results["main_table_found"] = True
                
                # Look for all possible tables with increasing index
                table_index = 2
                while True:
                    table_xpath = f'/html/body/form/table[2]/tbody/tr/td/table[2]/tbody/tr/td/table[{table_index}]'
                    tables = await page.query_selector_all(table_xpath)
                    
                    if not tables:
                        # No more tables found with this index
                        break
                    
                    for table in tables:
                        table_data = {
                            "table_index": table_index,
                            "entries": []
                        }
                        
                        # Extract rows from the table
                        rows = await table.query_selector_all('tr')
                        for row in rows:
                            # Extract cells from each row
                            cells = await row.query_selector_all('td')
                            if cells:
                                row_data = {}
                                # Try to identify content based on cell position or labels
                                for i, cell in enumerate(cells):
                                    # Extract text content
                                    text = await cell.text_content()
                                    text = text.strip() if text else ""
                                    
                                    # Try to identify if this is a signoff, status, date, or comment field
                                    if "name" in text.lower() or "signoff" in text.lower():
                                        row_data["signoff_name"] = text
                                    elif "status" in text.lower():
                                        row_data["status"] = text
                                    elif any(date_word in text.lower() for date_word in ["date", "time", "created", "modified"]):
                                        row_data["date"] = text
                                    elif "comment" in text.lower():
                                        row_data["comment"] = text
                                    else:
                                        # For cells without clear identification, store with index
                                        row_data[f"field_{i}"] = text
                                
                                if row_data:
                                    table_data["entries"].append(row_data)
                        
                        results["status_tables"].append(table_data)
                    
                    # Move to the next table index
                    table_index += 1
                
                # Extract data from specific tables if they exist
                for specific_table_index in [5]:
                    detail_table_xpath = f'/html/body/form/table/tbody/tr/td/a/table[2]/tbody/tr/td/table[{specific_table_index}]'
                    detail_tables = await page.query_selector_all(detail_table_xpath)
                    
                    if detail_tables:
                        detail_data = {
                            "table_index": specific_table_index,
                            "entries": []
                        }
                        
                        for detail_table in detail_tables:
                            # Extract rows
                            rows = await detail_table.query_selector_all('tr')
                            for row in rows:
                                cells = await row.query_selector_all('td')
                                if cells:
                                    entry = {}
                                    
                                    # Try to identify content based on known patterns
                                    for i, cell in enumerate(cells):
                                        text = await cell.text_content()
                                        text = text.strip() if text else ""
                                        if "signoff" in text.lower() or i == 0:  # Assuming first column might be signoff name
                                            entry["signoff_name"] = text
                                        elif "status" in text.lower() or i == 1:  # Assuming second column might be status
                                            entry["status"] = text
                                        elif "date" in text.lower() or i == 2:  # Assuming third column might be date
                                            entry["date"] = text
                                        elif "comment" in text.lower() or i >= 3:  # Assuming later columns might be comments
                                            entry["comment"] = text
                                        else:
                                            entry[f"field_{i}"] = text
                                    
                                    if entry:
                                        detail_data["entries"].append(entry)
                        
                        if detail_data["entries"]:
                            results[f"detail_table_{specific_table_index}"] = detail_data
            
            # Close the browser
            await browser.close()
            
            return results
    
    except Exception as e:
        print(f"Error processing the webpage: {e}", file=sys.stderr)
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Scrape SELC webpage tables')
    parser.add_argument('url', help='URL of the SELC webpage to scrape')
    parser.add_argument('-o', '--output', help='Output JSON file path (default: stdout)')
    args = parser.parse_args()
    
    # Run the async scraper
    results = asyncio.run(scrape_selc_webpage(args.url))
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Results written to {args.output}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
