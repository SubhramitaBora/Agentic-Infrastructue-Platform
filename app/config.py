import os

from dotenv import load_dotenv


load_dotenv()


JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "AD")


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "SubhramitaBora")
GITHUB_REPO = os.getenv("GITHUB_REPO", "Agentic-Workflow")

HYDRA_LITELLM_BASE_URL = os.getenv("HYDRA_LITELLM_BASE_URL")
HYDRA_API_KEY = os.getenv("HYDRA_API_KEY")
HYDRA_MODEL = os.getenv("HYDRA_MODEL")
HYDRA_TIMEOUT = int(os.getenv("HYDRA_TIMEOUT", "120"))