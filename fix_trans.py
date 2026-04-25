file_path = 'translations.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\\\\n', '\\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
