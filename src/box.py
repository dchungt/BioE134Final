from dataclasses import dataclass, field
from typing import List, Optional
from src.sample import Sample, Concentration, Culture
import os


@dataclass
class Box:
    name: str
    description: str
    location: str

    # 8x12 grid of samples, None if empty
    samples: List[List[Optional[Sample]]] = field(default_factory=lambda: [[None] * 12 for _ in range(8)])

    def __init__(self, name: str, description: str, location: str, rows: int, columns: int):
        self.name = name
        self.description = description
        self.location = location
        self.samples = [[None for _ in range(columns)] for _ in range(rows)]

    def is_empty(self):
        return all(sample is None for row in self.samples for sample in row)

    def box_to_tsv(self, filepath: str) -> str:
        # Check if the box's samples attribute is a 2D list with some length
        if not all(isinstance(row, list) for row in self.samples) or not self.samples:
            raise ValueError("The box must have 2D array of samples with some length.")

        # Ensure the filepath is valid
        if not os.path.exists(os.path.dirname(filepath)) or not os.path.isdir(os.path.dirname(filepath)):
            raise ValueError("The specified file path is invalid.")

        try:
            # Open the file and write the contents
            with open(filepath, 'w', newline='') as file:
                for row_index, row in enumerate(self.samples):
                    for col_index, sample in enumerate(row):
                        # Location in 2D array is one column in TSV
                        location = f"{row_index},{col_index}"
                        # Name in 2D array is the 2nd column in TSV
                        # If the sample is None, write an empty string
                        name = sample.label if sample else ""
                        file.write(f"{location}\t{name}\n")
        except IOError as e:
            raise IOError(f"An error occurred while writing to the TSV file: {e}")

        return f"TSV file created at {filepath}"

    @staticmethod
    def tsv_to_box(file_path: str) -> 'Box':
        # Check if the file path is valid and the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at {file_path} does not exist.")

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                box_metadata = lines[0].strip().split('\t')
                box_name, box_description, box_location = box_metadata

                samples = []
                for line in lines[1:]:
                    sample_data = line.strip().split('\t')
                    row, col, label = int(sample_data[0]), int(sample_data[1]), sample_data[2]

                    while len(samples) <= row:
                        samples.append([])
                    while len(samples[row]) <= col:
                        samples[row].append(None)

                    if label:
                        # Assuming the label is enough to create a Sample object; adjust as needed
                        samples[row][col] = Sample(label=label, sidelabel='', concentration=Concentration.DEFAULT_VALUE,
                                                   construct='', culture=Culture.DEFAULT_VALUE, clone='')

                return Box(name=box_name, description=box_description, location=box_location, samples=samples)
        except Exception as e:
            raise IOError(f"Error reading or processing the TSV file: {e}")
