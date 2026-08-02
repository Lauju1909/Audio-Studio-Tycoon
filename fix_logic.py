
with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Revert the bad replacement
content = content.replace("from managers.corporate_warfare import CorporateWarfareManager\nfrom models import ", "from models import ")

# Put the import at the very top, safely after standard library imports
content = content.replace("import os\n", "import os\nfrom managers.corporate_warfare import CorporateWarfareManager\n")

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Logic fixed.")
