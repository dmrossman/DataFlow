import re
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class ParsedData:
    date: str
    attributes_8: Dict[str, str] = field(default_factory=dict)
    attributes_48: Dict[str, List[str]] = field(default_factory=dict)

    def write_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            # Write the date
            file.write(f"{self.date}\n\n")

            # Write the 8 attributes
            for key, value in self.attributes_8.items():
                file.write(f"{key}\t{value}\n")

            file.write("\n")

            # Write the 48 attributes
            for key, values in self.attributes_48.items():
                file.write(f"{key}\t{values[0]}\t{values[1]}\t{values[2]}\n")

    def parse_file(self, file_path: str) -> ParsedData:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extract the date from the first line
        self.date = lines[0].strip()

        # Extract the next 8 lines of attributes and their values
        self.attributes_8 = {}
        for i in range(2, 10):
            line = lines[i].strip()
            key, value = re.split(r'\s{2,}', line)
            self.attributes_8[key] = value

        # Extract the next 48 lines of attributes and their three values
        self.attributes_48 = {}
        for i in range(10, 58):
            line = lines[i].strip()
            parts = re.split(r'\s{2,}', line)
            key = parts[0]
            values = parts[1:]
            self.attributes_48[key] = values

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

# Write the parsed data back to a file
output_file_path = '/c:/Users/DRossman/OneDrive - Coherent Corporation/Documents/GitHub/DataFlow/IDLs/output_565442_202411121320.1'
parsed_data.write_to_file(output_file_path)