# https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=dzQoOVFdSWDwKkNcvq60RcJGDqeR6pHP&scope=manage%3Ajira-project%20write%3Ajira-work%20read%3Ajira-work%20offline_access&redirect_uri=https%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback&state=${YOUR_USER_BOUND_VALUE}&response_type=code&prompt=consent
import requests

# 🔐 Step 1: Exchange authorization code for access + refresh tokens
def get_tokens(client_id, client_secret, code, redirect_uri):
    url = "https://auth.atlassian.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    response = requests.post(url, json=payload)
    return response.json()

# 🔁 Step 2: Refresh the access token using the refresh token
def refresh_access_token(client_id, client_secret, refresh_token):
    url = "https://auth.atlassian.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    response = requests.post(url, json=payload)
    return response.json()

# 🆔 Step 3: Get cloud ID
def get_cloud_id(access_token):
    url = "https://api.atlassian.com/oauth/token/accessible-resources"
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.get(url, headers=headers).json()


# 🔧 Set credentials
client_id = ""
client_secret = ""
redirect_uri = ""
code = ""
# 🎟️ Step 1: Get initial tokens
token_data = get_tokens(client_id, client_secret, code, redirect_uri)
print("Initial Token Response:", token_data)

access_token = token_data["access_token"]
refresh_token = token_data["refresh_token"]
print("Access Token:", access_token)
print("Refresh Token:", refresh_token)

# 🧭 Step 2: Get Cloud ID
cloud_id_data = get_cloud_id(access_token)
print("Cloud ID Response:", cloud_id_data)


# 🔁 Step 3: Simulate refresh when token expires
print("\n--- Simulating Token Expiry and Refresh ---")
new_token_data = refresh_access_token(client_id, client_secret, refresh_token)
print("New Access Token:", new_token_data.get("access_token"))
