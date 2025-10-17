from bs4 import BeautifulSoup

# Read the HTML file
with open("pure_case_data.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# --- Smart search: find table that *contains* expected columns ---
table = None
for t in soup.find_all("table"):
    headers = [th.get_text(strip=True).lower() for th in t.find_all("th")]
    if any(h in headers for h in ["sr no", "cases", "party name", "advocate"]):
        table = t
        break

if not table:
    print("❌ No suitable table found in HTML.")
else:
    print("✅ Table found with id:", table.get("id"))
    print("Extracting rows...\n")

    # Extract rows
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)

    # Display results
    for row in rows:
        print(row)
