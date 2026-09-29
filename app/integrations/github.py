import httpx

from app.config import GITHUB_TOKEN

GITHUB_API_URL = "https://api.github.com"


def github_headers():
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"

    payload = {
        "title": title,
        "body": body,
    }

    response = httpx.post(
        url,
        json=payload,
        headers=github_headers(),
        timeout=30,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"GitHub API error {response.status_code}: {response.text}"
        )

    return response.json()


def get_issue(
    owner: str,
    repo: str,
    issue_number: int,
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/issues/{issue_number}"
    )

    response = httpx.get(
        url,
        headers=github_headers(),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_repository(
    owner: str,
    repo: str,
):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"

    response = httpx.get(
        url,
        headers=github_headers(),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
):
    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/pulls/{pull_number}"
    )

    response = httpx.get(
        url,
        headers=github_headers(),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()