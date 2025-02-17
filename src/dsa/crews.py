from dsa.tasks import RenameTask, SortTask
from dsa.agents import PDFAnalystAgent
from crewai import Crew
from typing import List
from pathlib import Path

# Setting up classes for different crews


class RenameCrew(Crew):
    def __init__(self, tools, llm, trained_model_path, output_log_file):
        agents = [PDFAnalystAgent(tools, llm)]
        tasks = [RenameTask(agents[0])]
        verbose = True
        Crew.__init__(self, agents=agents, tasks=tasks, verbose=verbose, trained_model_path=trained_model_path, output_log_file=output_log_file)

class SortCrew(Crew):
    def __init__(self, tools, llm, directory_tree: List[Path], trained_model_path, output_log_file):
        agents = [PDFAnalystAgent(tools, llm)]
        tasks = [SortTask(agents[0], directory_tree)]
        verbose = True
        Crew.__init__(self, agents=agents, tasks=tasks, verbose=verbose, trained_model_path=trained_model_path, output_log_file=output_log_file)
