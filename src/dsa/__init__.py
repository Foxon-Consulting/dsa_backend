from pathlib import Path
from crewai import LLM
from typing import List
import os

RENAME_OPENAI_API_KEY = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo"
)

def get_tree(root_folder: Path) -> List[Path]:
    return [p for p in root_folder.rglob("*") if p.is_dir()]

def get_suggested_file_name(source_file_path: Path, llm: LLM = RENAME_OPENAI_API_KEY) -> str:
    """
    Rename the file using the RenameCrew class.
    """
    from dsa.crews import RenameCrew
    from crewai_tools import PDFSearchTool

    rename_custom_crew = RenameCrew(
        [PDFSearchTool(pdf=str(source_file_path))], llm
    )
    final_name = rename_custom_crew.kickoff().raw

    return final_name

def get_suggested_path(root_folder: Path, source_file_path: Path, llm: LLM = RENAME_OPENAI_API_KEY) -> Path:
    """
    Get the suggested path for the file using the SortCrew class.
    """
    from dsa.crews import SortCrew
    from crewai_tools import PDFSearchTool

    sort_custom_crew = SortCrew(
        [PDFSearchTool(pdf=str(source_file_path))], llm, get_tree(root_folder)
    )
    suggested_path = sort_custom_crew.kickoff().raw

    return suggested_path
