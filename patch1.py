import sys

with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

merch_class = '''
class MerchCampaign:
    """Eine Merchandising-Kampagne (T-Shirts, Figuren, etc.)"""
    def __init__(self, game_name, merch_type, duration_weeks, investment):
        self.game_name = game_name
        self.merch_type = merch_type
        self.duration_weeks = duration_weeks
        self.weeks_active = 0
        self.investment = investment
        self.total_revenue = 0

    def to_dict(self):
        return {
            "game_name": self.game_name,
            "merch_type": self.merch_type,
            "duration_weeks": self.duration_weeks,
            "weeks_active": self.weeks_active,
            "investment": self.investment,
            "total_revenue": self.total_revenue
        }

    @staticmethod
    def from_dict(data):
        m = MerchCampaign(
            data["game_name"],
            data["merch_type"],
            data["duration_weeks"],
            data["investment"]
        )
        m.weeks_active = data.get("weeks_active", 0)
        m.total_revenue = data.get("total_revenue", 0)
        return m
'''

if 'class MerchCampaign' not in content:
    content += '\n' + merch_class
    with open('models.py', 'w', encoding='utf-8') as f:
        f.write(content)
