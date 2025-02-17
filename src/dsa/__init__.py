from pathlib import Path
from crewai import LLM
from typing import List
import os

MODEL = "gpt-3.5-turbo"

RENAME_OPENAI_API_KEY = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=MODEL
)


def get_tree(root_folder: Path) -> List[Path]:
    return [p for p in root_folder.rglob("*") if p.is_dir()]

def get_suggested_file_name(source_file_path: Path, llm: LLM = RENAME_OPENAI_API_KEY) -> str:
    """
    Rename the file using the RenameCrew class.
    """
    from dsa.crews import RenameCrew
    from crewai_tools import PDFSearchTool

    search_tool =  PDFSearchTool(pdf=str(source_file_path))
    log_file_name = type(search_tool).__name__ + "_" + llm.model + "_log.txt"

    rename_custom_crew = RenameCrew(
        [search_tool], llm,trained_model_path="rename.pkl", output_log_file=log_file_name
    )
    final_name = rename_custom_crew.kickoff().raw

    return final_name

def get_suggested_path(root_folder: Path, source_file_path: Path, llm: LLM = RENAME_OPENAI_API_KEY) -> str:
    """
    Get the suggested path for the file using the SortCrew class.
    """
    from dsa.crews import SortCrew
    from crewai_tools import PDFSearchTool

    search_tool =  PDFSearchTool(pdf=str(source_file_path))
    log_file_name = type(search_tool).__name__ + "_" + llm.model + "_log.txt"

    sort_custom_crew = SortCrew(
        [search_tool], llm, get_tree(root_folder), trained_model_path="sort.pkl", output_log_file=log_file_name
    )
    suggested_path = sort_custom_crew.kickoff().raw

    return suggested_path
