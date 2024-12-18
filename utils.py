import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_press_website(year):
    search_url = f"https://press.spglobal.com/index.php?s=2429&l=100&year={year}&keywords=%22Set%2Bto%2BJoin%22"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    result_list = soup.find("ul", class_="wd_layout-simple wd_item_list")
    if not result_list:
        print(f"No results found for year {year}.")
        return []
    urls = [link.get("href") for link in result_list.find_all("a", href=True)]
    return urls


def extract_table_from_url(url):
    printable_url = url + "?printable=1"
    response = requests.get(printable_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table")
    if not table:
        print(f"No table found in the page: {url}")
        return None
    headers = ["Announced"]
    data = []
    header_row = table.find("tr")
    if not header_row:
        print(f"No header row found in the table: {url}")
        return None
    raw_headers = header_row.find_all("td")
    normalized_headers = []
    for th in raw_headers:
        header_text = ' '.join(th.stripped_strings)
        header_text = header_text.replace('\n', ' ').strip()
        if header_text in ["GICSSector", "GICS Sub-Industry"]:
            header_text = "GICS Sector"
        elif header_text in ["EffectiveDate"]:
            header_text = "Effective Date"
        normalized_headers.append(header_text)
    headers.extend(normalized_headers)
    headers.append("Event_Type")
    print(f"Extracted Headers: {headers}")  # Debugging statement
    announcement_span = soup.find("span", class_="xn-chron")
    announcement_date = announcement_span.get_text(strip=True) if announcement_span else "Unknown Date"
    page_text = soup.get_text().lower()
    event_type = "Index Review" if "quarterly rebalance" in page_text else "Corporate Action"
    for row in table.find_all("tr")[1:]:  # Skip header row
        cols = row.find_all("td")
        row_data = [announcement_date] + [col.get_text(strip=True) for col in cols] + [event_type]
        if len(row_data) == len(headers):
            data.append(row_data)
        else:
            print(f"Skipping row due to column mismatch: {row_data}")
    
    df = pd.DataFrame(data, columns=headers) if data else None
    
    if df is not None:
        if "Effective Date" in df.columns:
            df["Effective Date"] = df["Effective Date"].replace("", pd.NA).ffill()
        else:
            print(f"Warning: 'Effective Date' column not found in {url}. Filling with 'Unknown Date'.")
            df["Effective Date"] = "Unknown Date"
        if "Index Name" in df.columns:
            df["Index Name"] = df["Index Name"].replace("", pd.NA).ffill()
        else:
            print(f"'Index Name' column missing in {url}. Attempting to extract from page title.")
            index_name = extract_index_name(soup)
            if index_name:
                df["Index Name"] = index_name
            else:
                print(f"Warning: 'Index Name' not found in table or page for {url}. Filling with 'Unknown Index'.")
                df["Index Name"] = "Unknown Index"
    return df

def extract_index_name(soup):
    if soup.title:
        title_text = soup.title.get_text(strip=True)
        try:
            parts = title_text.split("Set to Join")
            if len(parts) > 1:
                index_part = parts[1].split("-")[0].strip()
                index_names = [name.strip() for name in index_part.split(";")]
                return "; ".join(index_names)
        except Exception as e:
            print(f"Error extracting 'Index Name' from title: {e}")
    index_header = soup.find("h1", class_="wd_title wd_language_left")
    if index_header:
        header_text = index_header.get_text(strip=True)
        try:
            parts = header_text.split("Set to Join")
            if len(parts) > 1:
                index_part = parts[1].split("-")[0].strip()
                index_names = [name.strip() for name in index_part.split(";")]
                return "; ".join(index_names)
        except Exception as e:
            print(f"Error extracting 'Index Name' from header: {e}")
    return None
