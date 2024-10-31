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
    for th in table.find("tr").find_all("td"):
        header_text = th.get_text(strip=True)
        if header_text in ["GICSSector", "GICS Sub-Industry"]:
            header_text = "GICS Sector"
        elif header_text in ["EffectiveDate"]:
            header_text = "Effective Date"
        headers.append(header_text)
    headers.append("Event_Type")
    announcement_date = soup.find("span", class_="xn-chron").get_text(strip=True) if soup.find("span", class_="xn-chron") else "Unknown Date"
    event_type = "Index Review" if "quarterly rebalance" in soup.get_text().lower() else "Corporate Action"
    for row in table.find_all("tr")[1:]:  # Skip header row
        cols = row.find_all("td")
        row_data = [announcement_date] + [col.get_text(strip=True) for col in cols] + [event_type]
        if len(row_data) == len(headers):
            data.append(row_data)
        else:
            print(f"Skipping row due to column mismatch: {row_data}")
    df = pd.DataFrame(data, columns=headers) if data else None
    if df is not None:
        df["Effective Date"] = df["Effective Date"].replace("", pd.NA).ffill()
        df["Index Name"] = df["Index Name"].replace("", pd.NA).ffill()
    return df