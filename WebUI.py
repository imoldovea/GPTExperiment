import openwebapi

# Assuming you've installed the openwebapi package:
# pip install openwebapi

# Initializing the API client
api_key = "YOUR_API_KEY" # Replace with your OpenWebAPI key
api_url = "https://api.openwebapi.io/v1"

client = openwebapi.Client(api_url, api_key)

# Example usage for a GET request
response = client.get("/endpoint")

if response.ok:
    data = response.json()
