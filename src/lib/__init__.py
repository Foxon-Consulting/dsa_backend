from pathlib import Path
from crewai import LLM
from typing import List
import os
import mimetypes
import PyPDF2
import io

from .crews import DocumentSortingAssistantCrew
# from .helper import convert_pdf_to_markdown


def suggest_filename(file: Path) -> str:
    """
    Suggest a filename for the file using the RenameCrew class.
    """
    print(f"Processing file for name suggestion: {file}")

    inputs = {
        "file": file
    }

    result = DocumentSortingAssistantCrew().suggest_filename_crew().kickoff(inputs=inputs)

    return result

def suggest_filedirectory(file: Path, directories: List[str]) -> str:
    """
    Suggest a directory for the file using the RenameCrew class.
    """
    print(f"Processing file {file} for directory suggestion: {directories}")

    inputs = {
        "file": file,
        "directories": directories
    }

    result = DocumentSortingAssistantCrew().suggest_directory_crew().kickoff(inputs=inputs)

    return result
