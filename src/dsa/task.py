from crewai import Task
from textwrap import dedent
from typing import List
from pathlib import Path


class RenameTask(Task):

    def __init__(self, agent):
        super().__init__(
            description=dedent(
                f"""
            Suggest a new name for the file, based on its content and date.

        """
            ),
            expected_output="propose a name for the file and its corresponding date (if it exists) with ONLY THE following format: '<year-month-day> <name of the file>'",
            agent=agent,
        )


class SortTask(Task):

    def __init__(self, agent, directory_tree: List[Path]):

        paths_string = ", ".join(str(p) for p in directory_tree)

        super().__init__(
            description=dedent(
                f"""
            According to the directory tree {paths_string}, suggest where the file should be placed depending on the content of the file AND display the new name result of task 1.
            the result of this task must ONLY BE THE PATH.

        """
            ),
            expected_output="DISPLAY ONLY THE PATH'",
            agent=agent,
        )
