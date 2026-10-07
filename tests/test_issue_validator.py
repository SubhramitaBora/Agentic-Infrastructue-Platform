import unittest

from app.agents.issue_validator import validate_jira_issue


class JiraIssueValidatorTests(unittest.TestCase):
    def test_accepts_well_formed_task(self):
        errors = validate_jira_issue({
            "project_key": "AD",
            "issue_type": "Task",
            "summary": "Document the gateway recovery steps",
            "description": (
                "Goal:\nDocument the recovery steps.\n\n"
                "Acceptance Criteria:\nThe runbook is reviewed and published."
            ),
            "priority": "Medium",
        })
        self.assertEqual(errors, [])

    def test_accepts_well_formed_bug(self):
        errors = validate_jira_issue({
            "project_key": "AD",
            "issue_type": "Bug",
            "summary": "Gateway returns intermittent errors",
            "description": (
                "Steps to Reproduce:\nSend requests during peak traffic.\n\n"
                "Expected Result:\nRequests complete successfully.\n\n"
                "Actual Result:\nSome requests return 504.\n\n"
                "Impact:\nSome users cannot complete requests."
            ),
            "priority": "High",
        })
        self.assertEqual(errors, [])

    def test_reports_missing_task_acceptance_criteria(self):
        errors = validate_jira_issue({
            "project_key": "AD",
            "issue_type": "Task",
            "summary": "Document gateway recovery steps",
            "description": "Goal:\nDocument the recovery steps.",
            "priority": "Medium",
        })
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["field"], "description.acceptance_criteria")
        self.assertEqual(errors[0]["text"], "[missing]")

    def test_reports_placeholder_as_missing_content(self):
        errors = validate_jira_issue({
            "project_key": "AD",
            "issue_type": "Task",
            "summary": "Document gateway recovery steps",
            "description": "Goal:\nNot provided\nAcceptance Criteria:\nTBD",
            "priority": "Medium",
        })
        self.assertEqual(
            {error["field"] for error in errors},
            {"description.goal", "description.acceptance_criteria"},
        )

    def test_reports_invalid_summary_and_project_key(self):
        errors = validate_jira_issue({
            "project_key": "bad/key",
            "issue_type": "Task",
            "summary": "short",
            "description": "Goal:\nDo work.\nAcceptance Criteria:\nWork is complete.",
            "priority": "Medium",
        })
        self.assertIn("project_key", {error["field"] for error in errors})
        self.assertIn("summary", {error["field"] for error in errors})

    def test_rejects_unsupported_issue_type(self):
        errors = validate_jira_issue({
            "project_key": "AD",
            "issue_type": "Story",
            "summary": "Implement recovery automation",
            "description": "Goal:\nAutomate recovery.\nAcceptance Criteria:\nRecovery is tested.",
            "priority": "Medium",
        })
        self.assertEqual(errors[0]["field"], "issue_type")


if __name__ == "__main__":
    unittest.main()
