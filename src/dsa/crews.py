from dsa.task import RenameTask, SortTask
from dsa.agent import PDFAnalystAgent
from crewai import Crew
from typing import List
from pathlib import Path

# Setting up classes for different crews

class RenameCrew(Crew):
    def __init__(self, tools, llm):
        agents = [PDFAnalystAgent(tools, llm)]
        tasks = [RenameTask(agents[0])]
        verbose = True
        Crew.__init__(self, agents=agents, tasks=tasks, verbose=verbose)

class SortCrew(Crew):
    def __init__(self, tools, llm, directory_tree: List[Path]):
        agents = [PDFAnalystAgent(tools, llm)]
        tasks = [SortTask(agents[0], directory_tree)]
        verbose = True
        Crew.__init__(self, agents=agents, tasks=tasks, verbose=verbose)
