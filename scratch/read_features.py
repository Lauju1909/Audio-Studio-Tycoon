import os

file_path = r"c:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\features_list.txt"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # Print in 500 character chunks to avoid truncation
        for i in range(0, len(content), 500):
            print(content[i:i+500])
            print("--- CHUNK END ---")
else:
    print(f"File not found: {file_path}")
