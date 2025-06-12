from crewai.tools import BaseTool
from typing import Optional, Type
import os
from pydantic import BaseModel, Field
from atlassian import Jira

class JiraTicketCreationInput(BaseModel):
    """Input model for Jira ticket creation."""
    summary: str = Field(..., description="Title/summary of the issue")
    description: str = Field(..., description="Description body of the issue")
    issue_type: Optional[str] = Field("Task", description="Type of issue")

class JiraTicketCreationTool(BaseTool):
    """Tool for creating Jira tickets."""
    name: str = "Jira Ticket Creation Tool"
    description: str = "A tool that creates Jira tickets with a summary, description, and issue type."
    args_schema: Type[BaseModel] = JiraTicketCreationInput

    def _run(self, summary: str, description: str, issue_type: str = "Task") -> str:
        """
        Create a Jira issue.

        Args:
            summary: Title/summary of the issue.
            description: Description body of the issue.
            issue_type: Type of issue (default: "Task").

        Returns:
            Created issue key (e.g., "SCRUM-123") or empty string if failed.
        """
        jira = Jira(
            url=os.getenv("JIRA_URL"),
            username=os.getenv("JIRA_USERNAME"),
            password=os.getenv("JIRA_PASSWORD"),
            cloud=True
        )
        try:
            project_key = os.getenv("JIRA_PROJECT_KEY")
            issue = jira.issue_create(fields={
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            })
            return issue["key"]
        except Exception as e:
            print(f"❌ Failed to create issue: {e}")
            return ""