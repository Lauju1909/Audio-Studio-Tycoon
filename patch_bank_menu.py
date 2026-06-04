import sys

with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add StockMarketMenu and AcquisitionMenu to BankMenu
bank_code = '''
            {'text': self.game_state.get_text('donate_menu'), 'action': lambda: "donation_menu"},
            {'text': self.game_state.get_text('menu_monetization'), 'action': lambda: "monetization_menu"}
        ]
'''
new_bank_code = '''
            {'text': self.game_state.get_text('donate_menu'), 'action': lambda: "donation_menu"},
            {'text': self.game_state.get_text('menu_monetization'), 'action': lambda: "monetization_menu"},
            {'text': self.game_state.get_text('stock_market_menu'), 'action': lambda: "stock_market_menu"},
            {'text': self.game_state.get_text('acquisition_menu_title'), 'action': lambda: "acquisition_menu"}
        ]
'''
content = content.replace(bank_code, new_bank_code)

with open('menus/business.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched BankMenu")
