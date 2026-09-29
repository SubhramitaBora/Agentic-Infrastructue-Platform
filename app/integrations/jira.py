import httpx

from app.config import (
    JIRA_BASE_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
)


def jira_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def jira_auth():
    return (
        JIRA_EMAIL,
        JIRA_API_TOKEN,
    )


def create_issue(
    project_key: str,
    summary: str,
    description: str,
    priority: str = "Medium",
):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            },
            "priority": {
                "name": priority
            }
        }
    }

    response = httpx.post(
        url,
        json=payload,
        headers=jira_headers(),
        auth=jira_auth(),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_issue(
    issue_key: str,
):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    response = httpx.get(
        url,
        headers=jira_headers(),
        auth=jira_auth(),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()