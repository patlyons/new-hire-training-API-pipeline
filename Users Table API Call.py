#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# For Python Tool In ALteryx

from ayx import Alteryx
import requests
import pandas as pd

# API settings
base_url = "https://api.training-example.com/api/v1.1/users"
username = "username"
api_key = "API123456"

page = 1
per_page = 1000
all_users = []


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
    users = data["users"]

    if not users:
        break

    all_users.extend(users)
    page += 1


# Convert to DataFrame
df = pd.DataFrame(all_users)

# Create users Table
users_df = df.drop(columns=["custom_user_field_data", "groups"], errors="ignore")

# Output to ALteryx
Alteryx.write(users_df, 1)

