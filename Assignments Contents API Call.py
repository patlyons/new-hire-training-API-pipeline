#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# For Python tool in Alteryx

from ayx import Alteryx
import requests
import pandas as pd

# API settings
base_url = "https://api.training-example.com/api/v1.1/assignments"
username = "xxx"
api_key = "APIKEY0123456789"

page = 1
per_page = 1000
all_assignments = []


# Function to recursively flatten contents
def extract_contents(contents):

    rows = []

    for item in contents:

        row = {
            "content_id": item.get("id"),
            "resource_type": item.get("resource_type"),
            "started_at": item.get("started_at"),
            "completed_at": item.get("completed_at"),
            "score": item.get("score"),
            "content_status": item.get("status")
        }

        rows.append(row)

        # If this item is a path with nested contents, flatten it
        if item.get("resource_type") == "path" and "contents" in item:
            rows.extend(extract_contents(item["contents"]))

    return rows


# Pull API data with pagination
while True:

    response = requests.get(
        base_url,
        auth=(username, api_key),
        params={
            "page": page,
            "per_page": per_page
        }
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    data = response.json()
    assignments = data["assignments"]

    if not assignments:
        break

    all_assignments.extend(assignments)

   # print(f"Pulled page {page}")
    page += 1


# Convert assignments to DataFrame
df = pd.DataFrame(all_assignments)


# Flatten contents into rows
content_rows = []

for _, row in df.iterrows():

    assignment_id = row["id"]

    if isinstance(row.get("contents"), list):

        extracted = extract_contents(row["contents"])

        for item in extracted:
            item["assignment_id"] = assignment_id
            content_rows.append(item)


contents_df = pd.DataFrame(content_rows)


# Send to Alteryx
Alteryx.write(contents_df, 1)


# In[ ]:




