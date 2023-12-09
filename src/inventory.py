from dataclasses import dataclass, field, replace
from typing import List, Dict, Set, Optional, Tuple
from location import Location
from box import Box
from sample import Sample, Culture, Concentration


@dataclass
class Inventory:
    boxes: List[Box] = field(default_factory=list)
    construct_to_locations: Dict[str, Set[Location]] = field(default_factory=dict)  # Quick lookup by construct name
    loc_to_conc: Dict[Location, Concentration] = field(default_factory=dict)  # Quick lookup by Concentration
    loc_to_clone: Dict[Location, str] = field(default_factory=dict)  # Quick lookup by Clone
    loc_to_culture: Dict[Location, Culture] = field(default_factory=dict)  # Quick lookup by Culture

    # Functions with Boxes

    def position_chooser(self) -> Optional[Tuple[str, int, int]]:
        for box in self.boxes:
            for row_index, row in enumerate(box.samples):
                for col_index, sample in enumerate(row):
                    if sample is None:
                        return box.name, row_index, col_index

        # If all boxes are full, return a signal to create a new box
        return None

    def add_box_to_inventory(self, input_box: Box) -> 'Inventory':

        # Check if the box is already in the inventory
        if any(box.name == input_box.name for box in self.boxes):
            raise ValueError(f"A box with the name {input_box.name} already exists in the inventory.")

        # Create a copy of the current inventory to maintain immutability
        new_inventory = replace(self)
        new_inventory.boxes.append(input_box)

        # Iterate through all samples in the input box and update dictionaries
        for row_index, row in enumerate(input_box.samples):
            for col_index, sample in enumerate(row):
                if sample:
                    location = Location(input_box.name, row_index, col_index, sample.label, sample.sidelabel)
                    new_inventory.loc_to_conc[location] = sample.concentration
                    new_inventory.loc_to_clone[location] = sample.clone
                    new_inventory.loc_to_culture[location] = sample.culture
                    if sample.construct not in new_inventory.construct_to_locations:
                        new_inventory.construct_to_locations[sample.construct] = set()
                    new_inventory.construct_to_locations[sample.construct].add(location)

        return new_inventory

    def remove_box(self, box_name: str):
        # Check if the box with the given name exists in the inventory
        box_to_remove = next((box for box in self.boxes if box.name == box_name), None)
        if not box_to_remove:
            raise ValueError(f"No box with the name {box_name} exists in the inventory.")

        # Create a new inventory instance to maintain immutability
        new_inventory = replace(self)
        new_inventory.boxes = [box for box in self.boxes if box.name != box_name]

        # Remove all locations associated with the removed box from the quick lookup dictionaries
        locations_to_remove = {loc for loc in new_inventory.construct_to_locations.keys() if loc == box_name}
        for loc in locations_to_remove:
            del new_inventory.loc_to_conc[loc]
            del new_inventory.loc_to_clone[loc]
            del new_inventory.loc_to_culture[loc]
            for construct, loc_set in new_inventory.construct_to_locations.items():
                if loc in loc_set:
                    loc_set.remove(loc)
                    if not loc_set:  # Remove the construct key if no locations left
                        del new_inventory.construct_to_locations[construct]

        return new_inventory

    def get_box_contents(self, box_name: str) -> List[List[Optional[Sample]]]:
        # Find the box with the given name
        box = next((b for b in self.boxes if b.name == box_name), None)
        if box is None:
            raise ValueError(f"Box named {box_name} does not exist in the inventory.")

        return box.samples

    def modify_box_metadata(self, box_before: Box, name: Optional[str] = None,
                            description: Optional[str] = None,
                            location: Optional[str] = None) -> 'Inventory':
        if box_before not in self.boxes:
            raise ValueError("The specified box does not exist in the inventory.")

        new_box = Box(name=name or box_before.name,
                      description=description or box_before.description,
                      location=location or box_before.location,
                      rows=len(box_before.samples),
                      columns=len(box_before.samples[0]))
        new_box.samples = box_before.samples  # Copy over the samples

        new_inventory = replace(self)
        new_inventory.boxes = [new_box if box.name == box_before.name else box for box in self.boxes]
        return new_inventory

    # Functions with samples in boxes in the inventory

    def add_sample(self, box_name: str, row: int, col: int, label: str, sidelabel: str,
                   concentration: Concentration, construct: str, culture: Culture, clone: str) -> 'Inventory':
        # Find the box with the given name
        box = next((b for b in self.boxes if b.name == box_name), None)
        if box is None:
            raise ValueError(f"Box named {box_name} does not exist in the inventory.")

        # Check if the specified location is within the bounds of the box
        if row >= len(box.samples) or col >= len(box.samples[0]):
            raise IndexError("The specified location is out of bounds.")

        # Check if the position is already occupied
        if box.samples[row][col] is not None:
            raise ValueError("Cannot place multiple samples in one position.")

        # Create the new sample and add it to the box
        new_sample = Sample(label=label, sidelabel=sidelabel, concentration=concentration,
                            construct=construct, culture=culture, clone=clone)
        new_samples = [list(row) for row in box.samples]  # Create a copy of the samples list
        new_samples[row][col] = new_sample

        # Create a new box with the updated samples
        new_box = Box(name=box.name, description=box.description, location=box.location,
                      rows=len(new_samples), columns=len(new_samples[0]))
        new_box.samples = new_samples

        # Update the inventory with the new box
        new_inventory = replace(self)
        new_inventory.boxes = [new_box if b.name == box_name else b for b in self.boxes]

        return new_inventory

    def remove_sample(self, box_name: str, row: int, col: int) -> 'Inventory':
        # Find the box with the given name
        box = next((b for b in self.boxes if b.name == box_name), None)
        if box is None:
            raise ValueError(f"Box named {box_name} does not exist in the inventory.")

        # Check if the specified location is within the bounds of the box
        if row >= len(box.samples) or col >= len(box.samples[0]):
            raise IndexError("The specified location is out of bounds.")

        # Check if the position is already empty
        if box.samples[row][col] is None:
            raise ValueError("There is no sample at the specified position.")

        # Create the new sample and add it to the box
        new_samples = [list(row) for row in box.samples]  # Create a copy of the samples list
        new_samples[row][col] = None

        # Create a new box with the updated samples
        new_box = Box(name=box.name, description=box.description, location=box.location,
                      rows=len(new_samples), columns=len(new_samples[0]))
        new_box.samples = new_samples

        # Create a new inventory instance to maintain immutability
        new_inventory = replace(self)
        new_inventory.boxes = [new_box if b.name == box_name else b for b in self.boxes]

        return new_inventory

    def find_sample(box: Box, sample: Sample) -> Location:
        for row_index, row in enumerate(box.samples):
            for col_index, s in enumerate(row):
                if s == sample:
                    return Location(box.name, row_index, col_index, sample.label, sample.sidelabel)
        raise ValueError("Sample not found in the given box.")
