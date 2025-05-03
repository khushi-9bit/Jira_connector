import requests

ACCESS_TOKEN = ""
CLOUD_ID = ""

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

BASE_API_URL = f"https://api.atlassian.com/ex/jira/{CLOUD_ID}/rest/api/3"

def create_issue(project_key, summary, description, issue_type="Task"):
    url = f"{BASE_API_URL}/issue"

    payload = {
        "fields": {
            "project": { "key": project_key },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}]
                }]
            },
            "issuetype": { "name": issue_type }
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        print(f"✅ Issue created: {response.json()['key']}")
        return response.json()
    else:
        print(f"❌ Failed to create issue: {response.status_code}, {response.text}")
        return None

def fetch_issues(project_key, max_results=10):
    url = f"{BASE_API_URL}/search"
    params = {
        "jql": f"project={project_key}",
        "maxResults": max_results
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        issues = response.json()["issues"]
        for issue in issues:
            print(f"{issue['key']}: {issue['fields']['summary']}")
        return issues
    else:
        print("❌ Failed to fetch issues:", response.status_code, response.text)
        return []

def update_issue(issue_key, summary=None, description=None):
    url = f"{BASE_API_URL}/issue/{issue_key}"
    fields = {}

    if summary:
        fields["summary"] = summary

    if description:
        fields["description"] = {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": description}]
            }]
        }

    response = requests.put(url, headers=HEADERS, json={"fields": fields})
    if response.status_code == 204:
        print(f"✅ Issue {issue_key} updated successfully.")
    else:
        print("❌ Failed to update issue:", response.status_code, response.text)


project_key = "SCRUM"

# # Create
created = create_issue(project_key, "OAuth API Test", "Issue created using OAuth 2.0")
# if created:
issue_key = created["key"]

#     # Fetch
fetch_issues(project_key)

    # Update
update_issue(issue_key, summary=f"{issue_key}Updated Summary via OAuth API")

