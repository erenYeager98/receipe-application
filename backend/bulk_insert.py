import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, Float, Integer, Text, JSON

# Database connection
engine = create_engine("mysql+pymysql://root:dk6969@localhost/recipes")

# Load JSON file
with open("US_recipes_null.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract relevant fields into list of dicts
records = []
for item in data.values():
    records.append({
        "cuisine": item.get("cuisine"),
        "title": item.get("title"),
        "rating": item.get("rating"),
        "prep_time": item.get("prep_time"),
        "cook_time": item.get("cook_time"),
        "total_time": item.get("total_time"),
        "description": item.get("description"),
        "nutrients": item.get("nutrients"),
        "serves": item.get("serves")
    })

# Convert to DataFrame
df = pd.DataFrame(records)

# Upload to MySQL
df.to_sql("recipes", con=engine, if_exists="append", index=False, dtype={
    "cuisine": VARCHAR(255),
    "title": VARCHAR(255),
    "rating": Float,
    "prep_time": Integer,
    "cook_time": Integer,
    "total_time": Integer,
    "description": Text,
    "nutrients": JSON,
    "serves": VARCHAR(255)
})

print("Bulk insert complete.")
