import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to patch _process_rivals
