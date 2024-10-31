# SP Global Press Release Scraper

This scraper focuses on gathering and organizing press release data from the SP Global website, particularly focusing on index change event types such as additions/deletions of stocks to/from SP Global indices as part of the constituents of the indices. These events are categorized as either index reviews and corporate actions. Index reviews includes quarterly rebalancing from the index review committee. Corporate actions include all events that are not index reviews such as but not limited to: bankcuptcies, mergers, acquisitions, public company going private, move to an OTC exchange, and ticker changes. 


## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Quickstart Example](#quickstart-example)
- [Details of `SPGlobalScraper`](#details-of-spglobalscraper)
  - [Function Reference for `utils.py`](#function-reference-for-utilspy)
- [File Output](#file-output)
  
## Overview
The code uses `sp_global_scraper.py` and utility functions in `utils.py` to extract and structure data in a usable format.  The scraper class `SPGlobalScraper` in `sp_global_scraper.py` manages the process of gathering data from SP Global’s press releases by year. 

Key features include:
- Extracting data across a specified period of time.
- Structuring columns for consistent output.

## Installation
To install and run this code, ensure you have the necessary Python packages:
```bash
pip install pandas requests beautifulsoup4
```

Clone or download this repository, then navigate to the project directory.

## Usage
### Quickstart Example
With the modules provided, you can run a complete scrape by simply creating an instance of `SPGlobalScraper` and using the `extract_tables_from_all_years` function. This script requires a start and end date in `YYYY-MM-DD` format, and the output will be saved in CSV format.

```python
from sp_global_scraper import SPGlobalScraper

# Run the scraper for 2021
scraper = SPGlobalScraper(start_date="2021-01-01", end_date="2021-12-31")
scraper.extract_tables_from_all_years()
```

This code will:
1. Retrieve relevant press release links.
2. Extract tables from each URL and log any URLs with no table.
3. Save the combined cleaned data into a CSV file.

## File Output
Running the scraper will save the results to a file named `press_releases_{start_year}_{end_year}.csv` in the working directory.

### Example Output Table

| Announced  | Effective_Date | Index_Name       | Action    | Company_Name         | Ticker | GICS_Sector           | Event_Type       |
|------------|----------------|------------------|-----------|----------------------|--------|------------------------|------------------|
| 9/24/2024  | 9/30/2024      | S&P 500         | Addition  | Amentum              | AMTM   | Industrials           | Corporate Action |
| 9/24/2024  | 10/1/2024      | S&P 500         | Deletion  | Bath & Body Works    | BBWI   | Consumer Discretionary| Corporate Action |
| 10/7/2024  | 10/11/2024     | S&P MidCap 400  | Addition  | DocuSign             | DOCU   | Information Technology| Corporate Action |
| 10/7/2024  | 10/11/2024     | S&P MidCap 400  | Deletion  | MDU Resources Group  | MDU    | Industrials           | Corporate Action |
| 10/7/2024  | 10/11/2024     | S&P SmallCap 600| Addition  | MDU Resources Group  | MDU    | Industrials           | Corporate Action |
| 10/7/2024  | 10/11/2024     | S&P SmallCap 600| Deletion  | Chuy's Holdings      | CHUY   | Consumer Discretionary| Corporate Action |

This structure is consistent, ensuring ease of analysis for the extracted data.

