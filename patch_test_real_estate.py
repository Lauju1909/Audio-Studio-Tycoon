
with open('test_real_estate.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("gs.money = 51_000_000", "gs.money = 51_000_000\n    gs.money = 300_000_000 # Make sure we can afford any property")

with open('test_real_estate.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched test_real_estate.py")
