import re
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class ParsedData:
    date: str
    attributes_8: Dict[str, str] = field(default_factory=dict)
    attributes_48: Dict[str, List[str]] = field(default_factory=dict)

def parse_file(file_path: str) -> ParsedData:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract the date from the first line
    date = lines[0].strip()

    # Extract the next 8 lines of attributes and their values
    attributes_8 = {}
    for i in range(2, 10):
        line = lines[i].strip()
        key, value = re.split(r'\s{2,}', line)
        attributes_8[key] = value

    # Extract the next 48 lines of attributes and their three values
    attributes_48 = {}
    for i in range(10, 58):
        line = lines[i].strip()
        parts = re.split(r'\s{2,}', line)
        key = parts[0]
        values = parts[1:]
        attributes_48[key] = values

    return ParsedData(date=date, attributes_8=attributes_8, attributes_48=attributes_48)

# Example usage
file_path = '/c:/Users/DRossman/OneDrive - Coherent Corporation/Documents/GitHub/DataFlow/IDLs/565442_202411121320.1'
parsed_data = parse_file(file_path)

print("Date:", parsed_data.date)
print("\nAttributes (8 lines):")
for key, value in parsed_data.attributes_8.items():
    print(f"{key}: {value}")

print("\nAttributes (48 lines):")
for key, values in parsed_data.attributes_48.items():
    print(f"{key}: {values}")