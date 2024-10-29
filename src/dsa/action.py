import os
import logging
from abc import ABC, abstractmethod

logging.getLogger().setLevel(logging.DEBUG)


class Action(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class RenameDocumentsBasedOnContentAndDate(Action):
    def __init__(self, source_folder_path):
        super().__init__()
        self.source_folder_path = source_folder_path

    def rename_document(self, document):
        logging.info(
            f"Execution of method rename_document with document {document}"
        )

    def execute(self):  # TODO: Implement this method
        files = [f for f in os.listdir(self.source_folder_path)]
        logging.debug(len(files))
        for file in files:
            self.rename_document(file)
        logging.info(
            f"Execution of class RenameDocumentsBasedOnContentAndDate with input {self.source_folder_path}"
        )


if __name__ == "__main__":

    source_folder_path_default = os.path.join(os.path.dirname(__file__), "dir")
    my_action = RenameDocumentsBasedOnContentAndDate(
        source_folder_path_default
    )
    my_action.execute()
