import requests
import os
from dotenv import load_dotenv
TOKEN_URL = "https://test.salesforce.com/services/oauth2/token"  # Use "https://login.salesforce.com" for production

# 🔹 Step 2: Get a New Access Token Using the Refresh Token
def get_access_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("SALESFORCE_CLIENT_ID"),
        "client_secret": os.getenv("SALESFORCE_CLIENT_SECRET"),
        "refresh_token": os.getenv("SALESFORCE_REFRESH_TOKEN"),
    }
    print(data)
    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()
    
    if "access_token" in response_data:
        print("✅ Successfully retrieved access token!")
        return response_data["access_token"], response_data["instance_url"]
    else:
        print("❌ Failed to get access token:", response_data)
        return None, None

# 🔹 Step 3: Query Salesforce Data Using SOQL
def query_salesforce(soql_query, access_token, instance_url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    query_url = f"{instance_url}/services/data/v59.0/query?q={soql_query}"
    print(query_url)  # Use latest API version
    response = requests.get(query_url, headers=headers)
    
    if response.status_code == 200:
        print("✅ Successfully retrieved data!")
        return response.json()["records"]
    else:
        print("❌ Failed to fetch data:", response.json())
        return None
if __name__ == "__main__":
    access_token, instance_url = get_access_token()
    
    if access_token and instance_url:
        # Corrected SOQL query to count the number of Account records
        soql_query = "SELECT FIELDS(ALL) from Territory2 limit 1"
        
        records = query_salesforce(soql_query, access_token, instance_url)
        print(records)