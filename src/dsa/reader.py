import langchain_community.document_loaders
import logging
import os


from langchain_community.document_loaders.image import UnstructuredImageLoader

from langchain_community.document_loaders.pdf import PyPDFLoader, PyPDFDirectoryLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from abc import ABC, abstractmethod

logging.getLogger().setLevel(logging.DEBUG)

absolute_path = os.path.dirname(__file__)

source_folder_path_default = os.path.join(absolute_path, "dir")
file_path_name_default = os.path.join(absolute_path, "dir/FAC0001.pdf")
image_path_name = os.path.join(absolute_path, "dir/image.jpg")

class Reader(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self):
        raise NotImplementedError

class DirectoryReader(Reader):
    def __init__(self, source_folder_path: str = source_folder_path_default):
        super().__init__()
        self.source_folder_path = source_folder_path_default

    def read(self):
        logging.info("Execution of class DirectoryReader")

        loader = DirectoryLoader(
            self.source_folder_path,
            show_progress=True
        )
        loaded_docs = loader.load()

        logging.debug(loaded_docs)
        return loaded_docs

class PdfDirectoryReader(Reader):
    def __init__(self, source_folder_path: str = source_folder_path_default):
        super().__init__()
        self.source_folder_path = source_folder_path_default

    def read(self):
        logging.info("Execution of class PDFDirectoryReader")

        loader = PyPDFDirectoryLoader(
            self.source_folder_path,
            show_progress=True
        )
        loaded_docs = loader.load()

        logging.debug(loaded_docs)
        return loaded_docs

class FileReader(Reader):
    def __init__(self, file_path_name: str = file_path_name_default):
        super().__init__()
        self.file_path_name = file_path_name_default


class PdfFileReader(FileReader):
    def __init__(self, file_path_name: str = file_path_name_default):
        super().__init__()
        self.file_path_name = file_path_name_default

    def read(self):
        logging.info("Execution of class PDFFileReader")

        loader = PyPDFLoader(
            file_path_name_default
        )
        loaded_docs = loader.load_and_split()
        return loaded_docs

class ImageLoader(Reader):
    def __init__(self):
        super().__init__()

    def read(self):
        logging.info("Execution of class ImageLoader")

        loader = UnstructuredImageLoader(
            image_path_name
        )

        loaded_docs = loader.load()
        return loaded_docs



if __name__ == "__main__":
    my_reader = ImageLoader()
    my_reader.read()
