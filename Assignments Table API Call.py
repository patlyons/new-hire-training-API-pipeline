#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# For Python tool in Alteryx

from ayx import Alteryx
import requests
import pandas as pd

base_url = "https://api.training-example.com/api/v1.1/assignments"

username = "username"
api_key = "api_key"

page = 1
per_page = 1000
all_assignments = []

# Pull API data with pagination
while True:

    response = requests.get(
        base_url,
        auth=(username, api_key),
        params={"page": page, "per_page": per_page}
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    data = response.json()
    assignments = data["assignments"]

    if not assignments:
        break

    all_assignments.extend(assignments)

    #print(f"Pulled page {page}")
    page += 1

# Convert to DataFrame
df = pd.DataFrame(all_assignments)

# Send to Alteryx output anchor 1
Alteryx.write(df, 1)

