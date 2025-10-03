#Decoder.py
#ECS101

from pathlib import Path
import pandas as pd
from typing import Dict, Tuple

dir = Path(__file__).resolve().parent 
COMPRESSION_PATH = pd.read_excel(dir / "compression_table.xlsx")

def bits_only(s: str):
    """keep only 0 and 1 from any input string."""
    return "".join(ch for ch in s if ch in "01")

def take_next_code(bits: str, codes: set[str], min_len: int, max_len: int):
    for length in range(min_len, max_len + 1): # try lengths from min to max
        code = bits[:length] #take the next length of bits
        if code in codes: #check if the code is valid else raise exception
            return code, bits[length:] #return values
    #exception 
    raise ValueError("no valid code found")

def load_compression(path: str):
    df = pd.read_excel(path)
    
    code_to_char = {
        str(row["Binary Code"]).strip(): str(row["Character"]) #map binary code to character ex: code_to_char = {"010": "A", "011": "B"} takes binary gets the corrposnding string values 
        for _, row in df.iterrows() #loops through each row of excel
        if pd.notna(row.get("Character")) and pd.notna(row.get("Binary Code")) #get rid of empty values
    }
    
    #exception 
    if not code_to_char:
        raise ValueError("missing or empty codebook")
    
    lengths = [len(code) for code in code_to_char.keys()] #find lengths of codes
    return code_to_char, min(lengths), max(lengths) #return all values needed


def decoder(input: str = dir / "BinOutput.txt", output: str = dir / "TextOutput.txt", compression_path: str = COMPRESSION_PATH):
    code_to_char, min_len, max_len = load_compression(compression_path)
    codes = set(code_to_char.keys())
    
    #reads only bits from input
    with open(input, "r", encoding="utf-8") as f:
        bits = bits_only(f.read())
        
    #decodes
    decoded = []
    while bits:
        code, bits = take_next_code(bits, codes, min_len, max_len) #process the next code 
        decoded.append(code_to_char[code]) #add it into the list
        
    #writes to output
    with open(output, "w", encoding="utf-8") as f:
        f.write("".join(decoded))
    print(f"Decoded text saved to {output}")
    
if __name__ == "__main__": #probs needs proper implimentation once figure out how pass txt into it 
    decoder()