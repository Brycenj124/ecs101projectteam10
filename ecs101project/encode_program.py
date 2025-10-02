import re
import pandas as pd
from pathlib import Path

var1 = pd.read_excel('compression_table.xlsx' , dtype = str)
print(var1)

def binary_to_str(text, table, regex):
    match = regex.match(text)  # only matches at start of string
    if not match:
        # return placeholder for unknown character
        return "#", text[1:]

    character = match.group(0)
    binary_code = table[character]

    return binary_code, text[len(character):]

def encode_file(input_file, output_file, table, regex):
    # Read the input file
    with open(input_file, "r") as f:
        text = f.read().strip()

    # Convert using regex matching
    binary_string = ""
    while text:
        code, text = binary_to_str(text, table, regex)
        binary_string += code

    # Count number of bits
    num_bits = len(binary_string)

    # Write result to output file
    with open(output_file, "w") as out:
        out.write(f"{num_bits}.{binary_string}")

if __name__ == "__main__":
    # Load allocation table from Excel
    df = pd.read_excel("compression_table.xlsx")
    allocation_table = dict(zip(df["Character"], df["Binary Code"]))

