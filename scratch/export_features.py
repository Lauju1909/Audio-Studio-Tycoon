import re
import os

file_path = r"c:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\features_list.txt"
output_path = r"c:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\scratch\features_detailed.md"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract features using regex
    features = re.findall(r"(\d+\.\s+\*\*.*?\*\*:.*?(?=\n\d+\.\s+\*\*|\n\n|\Z))", content, re.DOTALL)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Geplante Features für Audio Studio Tycoon\n\n")
        for i, feature in enumerate(features, 1):
            f.write(f"## Feature {i}\n")
            f.write(feature.strip() + "\n\n")
    print(f"Features written to {output_path}")
else:
    print("File not found")
