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

    def execute(self):
        logging.info("Exectuiton of class RenameDocumentsBasedOnContentAndDate")

class SampleAction(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        logging.info("Execution of class SampleAction")


if __name__ == "__main__":
    my_action = RenameDocumentsBasedOnContentAndDate("data")
    my_action.execute()
