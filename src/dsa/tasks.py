from crewai import Task
from textwrap import dedent
from typing import List
from pathlib import Path


class RenameTask(Task):

    def __init__(self, agent):
        super().__init__(
            description=dedent(
                f"""
            Suggest a new name for the file, based on its content and date. Use any tools you need to undestand the content of the pdf file.

        """
            ),
            expected_output="suggest a name for the file and its corresponding date (if it exists) and in corelation of it content with ONLY THE following format: '<year-month-day> <name of the file>'. Use any tools you need to undestand the content of the pdf file BUT ALWAYS DISPLAY THE ANSWER IN THE FORMAT '<year-month-day> <name of the file>'",
            agent=agent,
        )


class SortTask(Task):

    def __init__(self, agent, directory_tree: List[Path]):

        paths_string = ", ".join(str(p) for p in directory_tree)

        super().__init__(
            description=dedent(
                f"""
            According to the directory tree {paths_string}, suggest where the file should be placed depending on the content of the pdf file.
            the result of this task must ONLY BE THE PATH. Use any tools you need to undestand the content of the pdf file and ALWAYS reffer to the directory tree {paths_string} to suggest the path.

        """
            ),
            expected_output="DISPLAY ONLY THE PATH'",
            agent=agent,
        )
