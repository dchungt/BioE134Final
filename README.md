# BioE134Final

Daniel Chung

Inventory Final Project

Implemented Box, Inventory, Location, Sample classes, and relevant tests.

Inventory Functions:
- position_chooser: chooses an empty position to add a sample
- add_box_to_inventory: checks if the box is already in the inventory, copies current inventory to maintain immutability, and updates with new box
- remove_box: checks for indicated box, creates new inventory to maintain immutability, removes all locations associated with the removed box
- get_box_contents: returns samples of a given box
- modify_box_metadata
- add_sample: replaces a box with a new box with an added sample
- remove_sample: replaces a box with a new box without a given sample
- find_sample: gives the location of a given sample


Box Functions:
- is_empty
- box_to_tsv: converts a box to a tsv file and returns the filepath
- tsv_to_box: converts a tsv from a given filepath into a box


Inventory Test:
- test_add_box_to_inventory
- test_remove_box
- test_get_box_contents
- test_modify_box_metadata
- test_add_sample
- test_remove_sample
- test_position_chooser


Box Test:
- test_box_initialization
- test_is_empty
- test_box_to_tsv (must input personal filepath)
- test_tsv_to_box (must input personal filepath)
