# Decoder.py
# ECS101
from pathlib import Path
import pandas as pd

dir = Path(__file__).resolve().parent
COMPRESSION_PATH = dir / ("compression_table.csv")


def bits_only(s: str):
    """keep only 0 and 1 from any input string."""
    return "".join(ch for ch in s if ch in "01")


def take_next_code(bits: str, codes: set[str], min_len: int, max_len: int):
    for length in range(min_len, max_len + 1):  # try lengths from min to max
        code = bits[:length]
        if code in codes:
            return code, bits[length:]
    # If we get here, no valid code was found
    raise ValueError(f"no valid code found - first {max_len} bits: {bits[:max_len]}")


def load_compression(path: str):
    df = pd.read_csv(path, dtype=str)

    code_to_char = {}
    for _, row in df.iterrows():
        if pd.notna(row.get("Character")) and pd.notna(row.get("Binary Code")):
            char = row["Character"]  # Don't convert to string or strip!
            code = str(row["Binary Code"]).strip()

            # Skip invalid entries
            if pd.isna(char) or not code or code == "nan":
                continue

            # NO SPECIAL HANDLING - just map directly
            code_to_char[code] = char

    if not code_to_char:
        raise ValueError("missing or empty codebook")

    lengths = [len(code) for code in code_to_char.keys()]
    return code_to_char, min(lengths), max(lengths)

def decoder(input: str = dir / "BinOutput.txt",
            output: str = dir / "TextOutput.txt",
            compression_path: str = COMPRESSION_PATH):
    code_to_char, min_len, max_len = load_compression(compression_path)
    codes = set(code_to_char.keys())

    # DEBUG: Show what codes we have
    print(f"Loaded {len(codes)} codes")
    print(f"Code lengths: min={min_len}, max={max_len}")
    print(f"Sample codes: {sorted(list(codes))[:10]}")

    # read encoded file
    with open('BinOutput.txt', "r", encoding="utf-8") as f:
        raw = f.read().strip()

    print(f"Raw file length: {len(raw)}")

    # remove prefix (everything before and including first ".")
    if "." in raw:
        prefix, bitstream = raw.split(".", 1)
        print(f"Bit count from prefix: {prefix}")
    else:
        bitstream = raw

    # keep only valid bits
    bits = bits_only(bitstream)

    print(f"Total bits to decode: {len(bits)}")
    print(f"First 50 bits: {bits[:50]}")

    decoded = []
    char_count = 0
    try:
        while bits:
            code, bits = take_next_code(bits, codes, min_len, max_len)
            decoded.append(code_to_char[code])
            char_count += 1
            if char_count % 100 == 0:  # Progress indicator
                print(f"Decoded {char_count} characters...")
    except ValueError as e:
        print(f"\nERROR after decoding {char_count} characters")
        print(f"Remaining bits ({len(bits)} total): {bits[:100]}")
        raise

    with open(output, "w", encoding="utf-8") as f:
        f.write("".join(decoded))

    print(f"\n✓ Successfully decoded {char_count} characters")
    print(f"Decoded text saved to {output}")


if __name__ == "__main__":
    decoder()