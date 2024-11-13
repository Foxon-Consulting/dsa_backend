from crewai import Task
from textwrap import dedent

# TODO: Implement CrewAI tasks
#1st Task Renamer
#2nd Task Sorter

class RenameTask(Task):

    def __init__(self, agent):
        super().__init__(
            description=dedent(
                f"""
            Suggest a new name for the file, based on its content and date.

        """
            ),
            expected_output="propose a name for the file and its corresponding date (if it exists) with the following format: '<year-month-day> <name of the file>'",
            agent=agent,
        )

class SortTask(Task):

    def __init__(self, agent, directory_tree):
        super().__init__(
            description=dedent(
                f"""
            According to the directory tree {directory_tree}, suggest where the file should be placed depending on the content of the file AND display the new name result of task 1.

        """
            ),
            expected_output="Sugesst a folder from the directory tree where the file should be placed according to the file's content AND display the new name result of task 1.",
            agent=agent,
        )
