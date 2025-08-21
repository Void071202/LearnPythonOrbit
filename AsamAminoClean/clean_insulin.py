import re
import os

folder = "insulin_data"

files = [f for f in os.listdir(folder) if f.endswith(".txt")]

if not files:
    raise FileNotFoundError("Tidak ada file .txt di folder insulin_data")

files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(folder, x)))
input_file = files[-1] 

print("Memproses file:", input_file)

with open(os.path.join(folder, input_file)) as f:
    raw_data = f.read()

cleaned = raw_data.replace("ORIGIN", "").replace("//", "")

cleaned = re.sub(r'[^a-zA-Z]', '', cleaned)

cleaned = cleaned.lower()

base_name = os.path.splitext(input_file)[0]
clean_file = f"{base_name}-clean.txt"
with open(os.path.join(folder, clean_file), "w") as f:
    f.write(cleaned)

print("Full sequence length:", len(cleaned))  

lsinsulin = cleaned[0:24]
binsulin = cleaned[24:54]
cinsulin = cleaned[54:89]
ainsulin = cleaned[89:110]

with open(os.path.join(folder, f"{base_name}-lsinsulin.txt"), "w") as f: f.write(lsinsulin)
with open(os.path.join(folder, f"{base_name}-binsulin.txt"), "w") as f: f.write(binsulin)
with open(os.path.join(folder, f"{base_name}-cinsulin.txt"), "w") as f: f.write(cinsulin)
with open(os.path.join(folder, f"{base_name}-ainsulin.txt"), "w") as f: f.write(ainsulin)

print("Signal sequence (lsinsulin):", len(lsinsulin))  
print("B-chain (binsulin):", len(binsulin))           
print("C-peptide (cinsulin):", len(cinsulin))         
print("A-chain (ainsulin):", len(ainsulin))           