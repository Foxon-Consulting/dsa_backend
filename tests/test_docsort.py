import unittest
from pathlib import Path, WindowsPath
from dsa import get_tree, get_suggested_file_name, get_suggested_path
from common.docsort import _docsort

class DocsortTest(unittest.TestCase):
    def setUp(self):
        # self.task = Task("Dummy task", False)
        pass

    def tearDown(self):
        # To be implemented if required
        pass

    # def test_docsort(self):
    #     self.assertEqual(
    #         _docsort("green", "blue"), {"argA": "green", "argB": "blue"}
    #     )

    def test_generate_tree(self):
        result = get_tree(root_folder=Path("tests/dir"))
        self.assertEqual(result, [WindowsPath('tests/dir/emails'), WindowsPath('tests/dir/meetings'), WindowsPath('tests/dir/quotes')])

    def test_get_suggested_file_name(self):
        result = get_suggested_file_name(source_file_path=Path("tests/temp_upload/temp_file.pdf"))
        self.assertIsInstance(result, str)

    def test_get_suggested_path(self):
        result = Path(get_suggested_path(root_folder=Path("tests/dir"), source_file_path=Path("tests/temp_upload/temp_file.pdf")))
        self.assertIsInstance(result, Path)
