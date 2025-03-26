import logging

logger = logging.getLogger(__name__)

class JiraUtils:
    def __init__(self, jira_client):
        """
        Initialize JiraUtils with a JIRA client.
        :param jira_client: JIRA client fixture
        """
        self.client = jira_client

    def create_issue(self, project_key, summary, description, issue_type="Task"):
        """
        Create a new issue in JIRA.
        :param project_key: JIRA project key (e.g., "TEST")
        :param summary: Summary of the issue
        :param description: Detailed description of the issue
        :param issue_type: Type of the issue (e.g., "Task", "Bug")
        :return: Created issue object
        """
        try:
            issue = self.client.create_issue(
                project=project_key,
                summary=summary,
                description=description,
                issuetype={"name": issue_type},
            )
            logger.info(f"Issue {issue.key} created successfully.")
            return issue
        except Exception as e:
            logger.error(f"Failed to create issue: {e}")
            raise

    def get_issue(self, issue_key):
        """
        Retrieve an issue from JIRA by its key.
        :param issue_key: Key of the issue (e.g., "TEST-1")
        :return: Issue object
        """
        try:
            issue = self.client.issue(issue_key)
            logger.info(f"Issue {issue_key} retrieved successfully.")
            return issue
        except Exception as e:
            logger.error(f"Failed to retrieve issue {issue_key}: {e}")
            raise

    def add_comment(self, issue_key, comment):
        """
        Add a comment to an existing JIRA issue.
        :param issue_key: Key of the issue (e.g., "TEST-1")
        :param comment: Comment text
        """
        try:
            self.client.add_comment(issue_key, comment)
            logger.info(f"Comment added to issue {issue_key}.")
        except Exception as e:
            logger.error(f"Failed to add comment to issue {issue_key}: {e}")
            raise