import unittest

from common.docsort import _docsort


class DocsortTest(unittest.TestCase):
    def setUp(self):
        # self.task = Task("Dummy task", False)
        pass

    def tearDown(self):
        # To be implemented if required
        pass

    def test_docsort(self):
        self.assertEqual(
            _docsort("green", "blue"), {"argA": "green", "argB": "blue"}
        )
