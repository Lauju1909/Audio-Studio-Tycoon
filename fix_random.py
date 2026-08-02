
with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("                    import random\n                    if random.random() < 0.005:",
                          "                    if __import__('random').random() < 0.005:")

content = content.replace("import random", "import random") # Wait, I will just use regex to remove that specific `import random`

# Let's be safer
content = content.replace("                    import random\n", "")

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed local import random")
