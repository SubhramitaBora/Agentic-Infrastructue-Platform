from app.agents.jira_agent import jira_agent


result = jira_agent(
    "Investigate intermittent API Gateway latency affecting the platform"
)

print(result)