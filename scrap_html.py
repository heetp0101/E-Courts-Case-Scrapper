import re
import json
from bs4 import BeautifulSoup
import pandas as pd

# === Step 1: Load the raw HTML (JSON) file ===
file_path = "debug_response.html"  # update if needed

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read().strip()

# === Step 2: Try to detect JSON and extract case_data field ===
case_html = None
try:
    data = json.loads(content)
    if "case_data" in data:
        case_html = data["case_data"]
        print("✅ Extracted 'case_data' HTML content from JSON.")
    else:
        print("⚠️ 'case_data' key not found in JSON. Will clean raw content instead.")
except json.JSONDecodeError:
    print("⚠️ Not valid JSON, treating content as raw HTML.")
    case_html = content

# === Step 3: Clean the extracted HTML ===
clean_html = case_html.replace("\\/", "/")
clean_html = re.sub(r"\\[tnr]", "", clean_html)
clean_html = re.sub(r"\s{2,}", " ", clean_html)

# === Step 4: Save final cleaned HTML for inspection ===
with open("pure_case_data.html", "w", encoding="utf-8") as f:
    f.write(clean_html)

print("💾 Cleaned HTML saved as 'pure_case_data.html' — open it in browser to verify.")

# === Step 5: Parse using BeautifulSoup ===
soup = BeautifulSoup(clean_html, "html.parser")

# === Step 6: Find table ===
table = soup.find("table", {"id": ["dispTable", "titlehid"]})

if not table:
    print("❌ No table found with id='dispTable'. Check 'pure_case_data.html'.")
else:
    # Extract headers
    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    # Extract rows
    data = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if cells:
            data.append(cells)

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers[:len(data[0])])

    print("\n✅ Extracted Table Data:\n")
    print(df)

    df.to_csv("extracted_cases.csv", index=False)
    print("\n💾 Table saved to 'extracted_cases.csv'")
