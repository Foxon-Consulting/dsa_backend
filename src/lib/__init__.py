from pathlib import Path
from typing import List

from .crews import DocumentSortingAssistantCrew


def suggest_filename(file: Path) -> str:
    """
    Suggest a filename for the file using the DocumentSortingAssistantCrew
    class.
    """
    print(f"Processing file for name suggestion: {file}")

    inputs = {"file": file}

    result = (
        DocumentSortingAssistantCrew()
        .suggest_filename_crew()
        .kickoff(inputs=inputs)
    )

    return result


def suggest_directory(file: Path, directories: List[str]) -> str:
    """
    Suggest a directory for the file using the DocumentSortingAssistantCrew
    class.
    """
    print(f"Processing file {file} for directory suggestion: {directories}")

    inputs = {"file": file, "directories": directories}

    result = (
        DocumentSortingAssistantCrew()
        .suggest_directory_crew()
        .kickoff(inputs=inputs)
    )

    return result
