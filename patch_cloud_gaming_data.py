import json

game_data_file = "game_data.py"

with open(game_data_file, "r", encoding="utf-8") as f:
    content = f.read()

new_research = """
    "cloud_gaming": {
        "name": "RES_CLOUD_GAMING",
        "description": "RES_CLOUD_GAMING_DESC",
        "cost": 1500000,
        "dev_points_required": 8000,
        "category": "marketing",
        "required_tech": ["digital_distribution"]
    },
"""

if '"cloud_gaming"' not in content:
    content = content.replace('"digital_distribution": {', new_research + '    "digital_distribution": {')
    with open(game_data_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Research added.")
else:
    print("Research already exists.")
