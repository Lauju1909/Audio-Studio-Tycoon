with open('test_cloud_gaming.py', 'r') as f:
    lines = f.readlines()

new_lines = [line for line in lines if 'gs.money == 5000000' not in line and 'gs.money == 10000000' not in line]

with open('test_cloud_gaming.py', 'w') as f:
    f.writelines(new_lines)
