from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from jira_ticket_agent_meeting.tools.jiraticket_tool import JiraTicketCreationTool
from jira_ticket_agent_meeting.tools.pdf_reader import PDFReaderTool
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class JiraTicketAgentMeeting():
    """JiraTicketAgentMeeting crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def ticket_understander(self) -> Agent:
        return Agent(
            config=self.agents_config['ticket_understander'], # type: ignore[index]
            tools=[PDFReaderTool()],
            verbose=True
        )

    @agent
    def jira_ticket_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['jira_ticket_creator'], # type: ignore[index]
            tools=[JiraTicketCreationTool()],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def meeting_ticket_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['meeting_ticket_extraction_task'], # type: ignore[index]

        )

    @task
    def jira_ticket_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['jira_ticket_creation_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JiraTicketAgentMeeting crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
