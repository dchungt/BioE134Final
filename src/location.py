from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    boxname: str  # The name of the box a sample is in
    row: int  # The row within the box, starting with 0
    col: int  # The column within the box, starting with 0
    label: str  # What's written on the top of the tube
    sidelabel: str  # What's written on the side of the tube
