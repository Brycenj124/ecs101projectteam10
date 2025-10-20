import pandas as pd
import re


def binary_to_str(text, table, regex):
    match = regex.match(text)  # only matches at start of string
    if not match:
        # return binary code for placeholder character
        placeholder_code = table.get("#", "11000011111")  # Use # code or default
        return placeholder_code, text[1:]

    character = match.group(0)
    binary_code = table[character]

    return binary_code, text[len(character):]


def encode_file(input_file, BinOutput, table, regex):
    # Read the input file with UTF-8 encoding
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Track unknown characters
    unknown_chars = set()

    # Convert using regex matching
    binary_string = ""
    original_text = text
    while text:
        match = regex.match(text)
        if not match:
            # Character not in table
            if text:
                unknown_chars.add(text[0])
            code = table.get("#", "11000011111")  # placeholder code
            text = text[1:]
        else:
            character = match.group(0)
            code = table[character]
            text = text[len(character):]
        binary_string += code

    # Report unknown characters
    if unknown_chars:
        print(f"\n⚠ WARNING: {len(unknown_chars)} unknown characters found:")
        for char in sorted(unknown_chars)[:20]:  # Show first 20
            print(f"  '{char}' (ASCII {ord(char)})")

    # Count number of bits
    num_bits = len(binary_string)

    # Write result to output file with UTF-8 encoding
    with open('BinOutput.txt', "w", encoding="utf-8") as out:
        out.write(f"{num_bits}.{binary_string}")


if __name__ == "__main__":
    # Load allocation table from CSV
    df = pd.read_csv("compression_table.csv", dtype=str)

    # Create the mapping
    allocation_table = {}
    for _, row in df.iterrows():
        if pd.notna(row.get("Character")) and pd.notna(row.get("Binary Code")):
            char = row["Character"]
            code = str(row["Binary Code"]).strip()

            if not pd.isna(char) and code and code != "nan":
                allocation_table[char] = code

    print(f"✓ Loaded {len(allocation_table)} characters from CSV")

    # DEBUG: Check critical characters
    print(f"  Space: {allocation_table.get(' ', 'MISSING')}")
    print(f"  Letter 'C': {allocation_table.get('C', 'MISSING')}")
    print(f"  Digit '0': {allocation_table.get('0', 'MISSING')}")

    # Create regex pattern (match longest strings first)
    sorted_chars = sorted(allocation_table.keys(), key=len, reverse=True)
    pattern = "|".join(re.escape(char) for char in sorted_chars)
    regex = re.compile(pattern)

    # Call the encode function
    encode_file(
        input_file="input.txt",
        BinOutput="BinOutput.txt",
        table=allocation_table,
        regex=regex
    )

    print("Encoding complete! BinOutput.txt created.")