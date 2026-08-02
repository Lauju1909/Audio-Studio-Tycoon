
with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_init = """        self.is_f2p = False
        self.is_remake = False
        self.is_port = False
        self.has_mtx = False
        self.has_movie_deal = False"""

if "self.has_movie_deal = False" not in content:
    content = content.replace("self.has_mtx = False", "self.has_mtx = False\n        self.has_movie_deal = False\n        self.release_week = 0")
else:
    # Just add release_week if missing
    if "self.release_week = 0" not in content:
        content = content.replace("self.has_movie_deal = False", "self.has_movie_deal = False\n        self.release_week = 0")

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched GameProject init")
