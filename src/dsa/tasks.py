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
            IMPORTANT: You must select a directory from ONLY the given list of available directories below. Do not invent or suggest paths that are not in this list.

            Available directories: {paths_string}

            Based on the content of the PDF file, suggest the most appropriate directory from the above list where the file should be placed.
            Do not create new directories or suggest paths that are not in the list.
            The result of this task must ONLY BE ONE EXACT PATH from the list above, with no additional text or commentary.

            Use any tools you need to understand the content of the PDF file, but your final answer must be an exact match to one of the directories in the list.
            """
            ),
            expected_output="ONLY the exact path selected from the available directory list. No additional text, explanations, or invented paths.",
            agent=agent,
        )
