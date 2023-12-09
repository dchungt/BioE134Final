import unittest
from src.inventory import Inventory
from src.box import Box
from src.sample import Sample, Concentration, Culture
from src.location import Location


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()
        self.box1 = Box(name="Box1", description="Test Box 1", location="Location1", rows=2, columns=2)
        self.sample1 = Sample(label="Sample1", sidelabel="Side1", concentration=Concentration.DEFAULT_VALUE,
                              construct="Construct1", culture=Culture.DEFAULT_VALUE, clone="Clone1")
        # Add a sample to the box
        self.box1.samples[0][0] = self.sample1

    def test_add_box_to_inventory(self):
        # Test adding a box to the inventory
        updated_inventory = self.inventory.add_box_to_inventory(self.box1)
        self.assertIn(self.box1, updated_inventory.boxes)

    def test_remove_box(self):
        # Test removing a box from the inventory
        updated_inventory = self.inventory.add_box_to_inventory(self.box1)
        updated_inventory = updated_inventory.remove_box("Box1")
        self.assertNotIn(self.box1, updated_inventory.boxes)

    def test_get_box_contents(self):
        # Test retrieving the contents of a box
        updated_inventory = self.inventory.add_box_to_inventory(self.box1)
        box_contents = updated_inventory.get_box_contents("Box1")
        self.assertEqual(box_contents, self.box1.samples)

    def test_modify_box_metadata(self):
        # Test modifying the metadata of a box
        updated_inventory = self.inventory.add_box_to_inventory(self.box1)
        updated_inventory = updated_inventory.modify_box_metadata(self.box1, name="Box1_New")
        modified_box = next(box for box in updated_inventory.boxes if box.name == "Box1_New")
        self.assertEqual(modified_box.name, "Box1_New")

    def test_add_sample(self):
        # Ensure the box has an empty position before adding a sample
        self.box1.samples[0][0] = None  # Make sure this position is empty
        updated_inventory = self.inventory.add_box_to_inventory(self.box1)
        updated_inventory = updated_inventory.add_sample("Box1", 0, 0, "Sample1", "Side1", Concentration.DEFAULT_VALUE,
                                                         "Construct1", Culture.DEFAULT_VALUE, "Clone1")
        self.assertIsNotNone(updated_inventory.boxes[0].samples[0][0])

    def test_remove_sample(self):
        # Add a sample and then remove it
        self.box1.samples[0][0] = None  # Make sure this position is empty
        updated_inventory = self.inventory.add_box_to_inventory(self.box1)
        updated_inventory = updated_inventory.add_sample("Box1", 0, 0, "Sample1", "Side1", Concentration.DEFAULT_VALUE,
                                                         "Construct1", Culture.DEFAULT_VALUE, "Clone1")
        updated_inventory = updated_inventory.remove_sample("Box1", 0, 0)
        self.assertIsNone(updated_inventory.boxes[0].samples[0][0])

    def test_position_chooser(self):
        # Test the position chooser function
        updated_inventory = self.inventory.add_box_to_inventory(self.box1)
        position = updated_inventory.position_chooser()
        self.assertIsNotNone(position)  # Assuming at least one position is available

    # Additional tests for other methods like find_sample can be added


if __name__ == '__main__':
    unittest.main()
