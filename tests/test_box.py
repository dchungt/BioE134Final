import unittest
import os
from src.box import Box
from src.sample import Sample, Concentration, Culture


class TestBox(unittest.TestCase):

    def setUp(self):
        # Set up a test box
        self.test_box = Box(name="TestBox", description="TestDescription", location="TestLocation", rows=2, columns=2)
        self.test_sample = Sample(label="TestSample", sidelabel="TestSideLabel",
                                  concentration=Concentration.DEFAULT_VALUE,
                                  construct="TestConstruct", culture=Culture.DEFAULT_VALUE, clone="TestClone")

    def test_box_initialization(self):
        # Test the initialization of a Box
        self.assertEqual(self.test_box.name, "TestBox")
        self.assertEqual(self.test_box.description, "TestDescription")
        self.assertEqual(self.test_box.location, "TestLocation")
        self.assertEqual(len(self.test_box.samples), 2)
        self.assertEqual(len(self.test_box.samples[0]), 2)

    def test_is_empty(self):
        # Test if the box is empty
        self.assertTrue(self.test_box.is_empty())

    # Input your own filepath to test code
    def test_box_to_tsv(self):
        # Test converting a box to a TSV file
        filepath = "USE/YOUR/FILEPATH.tsv"
        result = self.test_box.box_to_tsv(filepath)
        self.assertTrue(os.path.exists(filepath))
        self.assertIn("TSV file created at", result)
        os.remove(filepath)  # Clean up the test file

    # Input your own filepath to test code
    def test_tsv_to_box(self):
        # Test creating a box from a TSV file
        filepath = "USE/YOUR/FILEPATH.tsv"
        self.test_box.samples[0][0] = self.test_sample
        self.test_box.box_to_tsv(filepath)

        new_box = Box.tsv_to_box(filepath)
        self.assertEqual(new_box.name, self.test_box.name)
        self.assertEqual(new_box.samples[0][0].label, self.test_sample.label)
        os.remove(filepath)  # Clean up the test file

    # Additional test methods can be added as needed


if __name__ == '__main__':
    unittest.main()
