# SP Global Press Release Scraper

This project provides a scraper for gathering and organizing press release data from the SP Global website, particularly focusing on event types such as index reviews and corporate actions. The code uses `sp_global_scraper.py` and utility functions in `utils.py` to extract and structure data in a usable format. 

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Quickstart Example](#quickstart-example)
- [Details of `SPGlobalScraper`](#details-of-spglobalscraper)
  - [Function Reference for `utils.py`](#function-reference-for-utilspy)
- [File Output](#file-output)
  
## Overview
The scraper class `SPGlobalScraper` in `sp_global_scraper.py` manages the process of gathering data from SP Global’s press releases by year. Key features include:
- Extracting data across multiple years.
- Structuring columns (e.g., merging `GICS Sector`, `GICSSector`, and `GICS Sub-Industry` columns) for consistent output.
- Forward-filling dates and index names where relevant data is implied.

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
2. Extract tables from each URL and standardize the column names.
3. Fill missing values in `Effective Date` and `Index Name`.
4. Save the combined data into a CSV file.

## Details of `SPGlobalScraper`
The `SPGlobalScraper` class in `sp_global_scraper.py` is responsible for:
1. **Initialization**: Setting the date range and identifying years to search.
2. **Extracting Data by Year**: Iterating through press releases to gather tables of interest.
3. **Saving Output**: Outputting the combined data to a CSV file.

### Function Reference for `utils.py`

#### `search_press_website(year)`
- **Purpose**: Searches the SP Global press release page for URLs of announcements in a given year.
- **Parameters**: `year` - Year to search as an integer.
- **Returns**: List of URLs matching the query.

#### `extract_table_from_url(url)`
- **Purpose**: Retrieves and standardizes table data from a press release URL.
- **Parameters**: `url` - Full URL of the press release page.
- **Returns**: DataFrame containing standardized data, with columns such as:
  - **GICS Sector**: Combines `GICSSector` and `GICS Sub-Industry` into `GICS Sector`.
  - **Effective Date**: Combines `EffectiveDate` with `Effective Date`.
- **Data Cleaning**: Forward fills empty cells in `Effective Date` and `Index Name`.

## File Output
Running the scraper will save the results to a file named `press_releases_{start_year}_{end_year}.csv` in the working directory.

Example of CSV structure:
| Announced     | Index Name      | GICS Sector | Effective Date | Event_Type       |
|---------------|-----------------|-------------|----------------|------------------|
| 2021-12-01    | S&P 500         | Financials  | 2021-12-15     | Corporate Action |
| ...           | ...             | ...         | ...            | ...              |

This structure is consistent regardless of original column names, ensuring ease of analysis for the extracted data.

