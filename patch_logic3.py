import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to clean up the elif r_game:\n            \n            if r_game: logic
content = content.replace("elif r_game:\n            \n            if r_game:", "elif r_game:")

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed indentation")
