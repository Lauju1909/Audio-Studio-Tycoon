import json

log_path = r"C:\Users\lauri\.gemini\antigravity\brain\56a43426-bbaf-4d42-ac7e-e5ee84c6ba72\.system_generated\logs\overview.txt"
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if "USER" in data.get("source", ""):
                print(f"KEYS: {list(data.keys())}")
                print(f"DATA: {data}")
                print("-" * 50)
        except Exception as e:
            print("ERROR", e)
