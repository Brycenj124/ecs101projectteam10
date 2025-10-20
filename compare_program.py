

def compare_files(original_file, decoded_file, encoded_file):
    # Read the original and decoded files
    with open(original_file, 'r', encoding='utf-8') as f1, open(decoded_file, 'r', encoding='utf-8') as f2:
        original_text = f1.read().strip()
        decoded_text = f2.read().strip()

    # Read the encoded file to get bit count
    with open(encoded_file, 'r', encoding='utf-8') as f3:
        encoded_content = f3.read().strip()
    bit_count = int(encoded_content.split('.', 1)[0]) if '.' in encoded_content else len(encoded_content)

    # Compare character by character
    total_chars = min(len(original_text), len(decoded_text))
    matches = sum(1 for i in range(total_chars) if original_text[i] == decoded_text[i])
    mismatches = total_chars - matches

    # Calculate percentage of match
    match_percent = 100 * matches / total_chars if total_chars > 0 else 0

    # Calculate percentage reduction
    reduction_percent = 100 * (8 * len(original_text) - bit_count) / (8 * len(original_text)) if len(original_text) > 0 else 0

    # Display results
    print("=== Compression Evaluation ===")
    print(f"Total characters compared: {total_chars}")
    print(f"Matches: {matches}")
    print(f"Mismatches: {mismatches}")
    print(f"% Level of Match: {match_percent:.2f}%")
    print(f"% Reduction: {reduction_percent:.2f}%")

if __name__ == "__main__":
    compare_files("input.txt", "TextOutput.txt", "BinOutput.txt")
