from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import FileReadTool
from .tools import DoclingMarkdownTool, DoclingTextTool

# Setting up classes for different crews
@CrewBase
class DocumentSortingAssistantCrew():
    name: str = "Document Sorting Assistant Crew"

    @agent
    def analyse_file_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['analyse_file_agent'],
            tools=[FileReadTool(), DoclingMarkdownTool(), DoclingTextTool()],
            verbose=True
        )

    @agent
    def suggest_file_name_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['suggest_file_name_agent'],
            verbose=True
        )

    @agent
    def suggest_directory_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['suggest_directory_agent'],
            verbose=True
        )

    @task
    def analyse_file_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyse_file_task'],
            output_file='/logs/analyse_file_task.md'
        )

    @task
    def suggest_file_name_task(self) -> Task:
        return Task(
            config=self.tasks_config['suggest_file_name_task'],
            output_file='/logs/suggest_file_name_task.md'
        )

    @task
    def suggest_directory_task(self) -> Task:
        return Task(
            config=self.tasks_config['suggest_directory_task'],
            output_file='/logs/suggest_directory_task.md'
        )

    @crew
    def suggest_filename_crew(self) -> Crew:
        return Crew(
            agents=[self.analyse_file_agent(), self.suggest_file_name_agent()],
            tasks=[self.analyse_file_task(), self.suggest_file_name_task()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def suggest_directory_crew(self) -> Crew:
        return Crew(
            name="Suggest Directory Crew",
            agents=[self.analyse_file_agent(), self.suggest_directory_agent()],
            tasks=[self.analyse_file_task(), self.suggest_directory_task()],
            process=Process.sequential,
            verbose=True,
        )
