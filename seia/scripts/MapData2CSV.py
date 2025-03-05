import requests
import re
import json
import pandas as pd

# Step 1: Fetch the data
url = "https://flo.uri.sh/visualisation/19069509/embed?auto=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise ValueError(f"Failed to fetch data: {response.status_code}")

# Step 2: Extract the regions array using regex
regions_pattern = re.compile(
    r'"regions"\s*:\s*(\[.*?\])\s*,\s*"regions_geometry"',
    re.DOTALL
)
match = regions_pattern.search(response.text)

if not match:
    print("Response snippet around 'regions':")
    print(response.text.split('"regions":')[1][:2000])  # Debug snippet
    raise ValueError("Could not find 'regions' array in the response.")

regions_js = match.group(1)

# Step 3: Clean non-JSON syntax
regions_js_cleaned = re.sub(
    r"new Date\((\d+)\)",
    lambda m: f'"{pd.to_datetime(int(m.group(1)), unit="ms").isoformat()}"',
    regions_js
)

# Step 4: Parse JSON
try:
    regions_data = json.loads(regions_js_cleaned)
except json.JSONDecodeError as e:
    print("Failed to parse JSON. Here's the cleaned JS snippet:")
    print(regions_js_cleaned)
    raise e

# Step 5: Extract and clean data
cleaned_data = []
for region in regions_data:
    metadata = region.get("metadata", [])
    state_info = {
        "State": region.get("id", ""),
        "Data Current Through": metadata[0] if len(metadata) > 0 else None,
        "Solar Installed (MW)": metadata[1] if len(metadata) > 1 else None,
        "National Ranking": metadata[2] if len(metadata) > 2 else None,
        "Enough Solar Installed to Power": metadata[3] if len(metadata) > 3 else None,
        "Percentage of State's Electricity from Solar": metadata[4] if len(metadata) > 4 else None,
        "Solar Jobs": metadata[5] if len(metadata) > 5 else None,
        "Link": metadata[6] if len(metadata) > 6 else None,
    }
    cleaned_data.append(state_info)

# Step 6: Create a DataFrame
df = pd.DataFrame(cleaned_data)
print(df)

# Step 7: Save the DataFrame to a CSV file (optional)
df.to_csv("data/state_solar_data.csv", index=False)