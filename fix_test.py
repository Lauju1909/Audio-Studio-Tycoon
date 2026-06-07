import sys

with open('test_cloud_gaming.py', 'r') as f:
    data = f.read()

data = data.replace('gs = GameState(DummyAudio())', 'gs = GameState()\ngs.audio = DummyAudio()')
data = data.replace('import pytest', 'import pytest\nimport logic')
with open('test_cloud_gaming.py', 'w') as f:
    f.write(data)
