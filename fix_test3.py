with open('test_cloud_gaming.py', 'r') as f:
    data = f.read()

data = data.replace('    def speak(self, text):\n        pass', '    def speak(self, text):\n        pass\n    def play_sound(self, file):\n        pass')

with open('test_cloud_gaming.py', 'w') as f:
    f.write(data)
