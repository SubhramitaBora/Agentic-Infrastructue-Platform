import httpx
import re

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


def search_issues(
    project_key: str,
    text: str | None = None,
    status: str | None = None,
    max_results: int = 10,
):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", project_key):
        raise ValueError("Invalid Jira project key.")
    clauses = [f'project = "{project_key.upper()}"']
    if text:
        escaped_text = text.replace("\\", "\\\\").replace('"', '\\"')
        clauses.append(f'text ~ "{escaped_text}"')
    if status:
        escaped_status = status.replace("\\", "\\\\").replace('"', '\\"')
        clauses.append(f'status = "{escaped_status}"')

    response = httpx.post(
        f"{JIRA_BASE_URL}/rest/api/3/search/jql",
        json={
            "jql": " AND ".join(clauses),
            "maxResults": min(max(max_results, 1), 20),
            "fields": ["summary", "status", "priority", "issuetype"],
        },
        headers=jira_headers(),
        auth=jira_auth(),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return [
        {
            "issue_key": issue["key"],
            "summary": issue.get("fields", {}).get("summary"),
            "status": (issue.get("fields", {}).get("status") or {}).get("name"),
            "priority": (issue.get("fields", {}).get("priority") or {}).get("name"),
            "issue_type": (issue.get("fields", {}).get("issuetype") or {}).get("name"),
        }
        for issue in data.get("issues", [])
    ]


def update_issue(
    issue_key: str,
    summary: str | None = None,
    description: str | None = None,
    priority: str | None = None,
):
    fields = {}
    if summary is not None:
        fields["summary"] = summary
    if description is not None:
        fields["description"] = {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": description}],
            }],
        }
    if priority is not None:
        fields["priority"] = {"name": priority}
    if not fields:
        raise ValueError("At least one Jira field must be provided to update.")

    response = httpx.put(
        f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}",
        json={"fields": fields},
        headers=jira_headers(),
        auth=jira_auth(),
        timeout=30,
    )
    response.raise_for_status()
    return {"key": issue_key, "updated_fields": list(fields)}
