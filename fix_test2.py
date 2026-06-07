with open('test_cloud_gaming.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'gs = GameState()' in line:
        new_lines.append(line)
        new_lines.append('    gs.audio = DummyAudio()\n')
    elif 'gs.audio = DummyAudio()' in line:
        pass
    else:
        new_lines.append(line)

with open('test_cloud_gaming.py', 'w') as f:
    f.writelines(new_lines)
