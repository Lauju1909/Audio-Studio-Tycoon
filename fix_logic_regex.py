import re

filepath = 'logic.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any occurrence of the wrongly inserted import
# Keep only the original `from models import ` with its original indentation
content = re.sub(r"[ \t]*from managers\.corporate_warfare import CorporateWarfareManager\n([ \t]*from models import )", r"\1", content)

# But we DO need it at the top of the file!
# Let's check if it's still at the top:
if 'from managers.corporate_warfare import CorporateWarfareManager' not in content:
    content = content.replace("import os\n", "import os\nfrom managers.corporate_warfare import CorporateWarfareManager\n")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Logic regex fixed.")
