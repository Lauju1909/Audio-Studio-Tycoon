with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('if self.is_public_company and year > self.last_shareholder_year:', "if getattr(self, 'is_public_company', False) and year > self.last_shareholder_year:")
content = content.replace('self.share_value = max(10, self.share_value - 20)', "self.share_value = max(10, getattr(self, 'share_value', 100) - 20)")
content = content.replace('self.share_value += 10', "self.share_value = getattr(self, 'share_value', 100) + 10")

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed logic.py")
