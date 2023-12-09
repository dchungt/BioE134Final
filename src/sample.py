from dataclasses import dataclass
from enum import Enum


class Culture(Enum):
    LIBRARY = "library"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    DEFAULT_VALUE = "default"


class Concentration(Enum):
    MINIPREP = "miniprep"  # A plasmid miniprep
    ZYMO = "zymo"  # A purified DNA product
    UM100 = "100uM"  # Oligo concentration for stocks
    UM10 = "10uM"  # Oligo concentration for PCR
    UM266 = "2.66uM"  # Oligo concentration for sequencing
    DIL20X = "20x dilution"  # A diluted plasmid or other DNA
    GENE = "gene"  # A gene synthesis order
    DEFAULT_VALUE = "default"


@dataclass(frozen=True)
class Sample:
    label: str  # What's written on the top of the tube
    sidelabel: str  # What's written on the side of the tube
    concentration: Concentration  # The amount or type of DNA present
    construct: str  # The name of the DNA matching the construction file
    culture: Culture  # For minipreps only, how many rounds of isolation
    clone: str  # Which isolate of several of the same construct
