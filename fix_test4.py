with open('test_cloud_gaming.py', 'r') as f:
    data = f.read()

data = data.replace('def speak(self, text):', 'def speak(self, text, interrupt=False):')

with open('test_cloud_gaming.py', 'w') as f:
    f.write(data)
