import re
import os

file_path = r"c:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\features_list.txt"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract features using regex
    features = re.findall(r"(\d+\.\s+\*\*.*?\*\*:.*?(?=\n\d+\.\s+\*\*|\n\n|\Z))", content, re.DOTALL)
    
    for i, feature in enumerate(features, 1):
        print(f"--- FEATURE {i} ---")
        print(feature.strip())
        print("-" * 20)
else:
    print("File not found")
