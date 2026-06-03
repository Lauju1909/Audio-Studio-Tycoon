import codecs

lines = []
with codecs.open('logic.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_block = """        # Konsolenentwicklung
        if getattr(self, "is_developing_console", False):
            self.console_progress += 1
            if self.console_progress >= getattr(self, 'console_total_weeks', 100):
                self.is_developing_console = False
                c = self.current_console_draft
                new_console = CustomConsole(
                    name=c['name'],
                    architecture=c.get('architecture', 'RISC'),
                    performance=c.get('performance', 1),
                    marketing_budget=c.get('marketing_budget', 0),
                    dev_cost=c['cost'],
                    release_week=self.week
                )
                if not hasattr(self, "custom_consoles"):
                    self.custom_consoles = []
                self.custom_consoles.append(new_console)
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hardware'),
                    subject=self.get_text('subject_console_done'),
                    body=self.get_text('body_console_done', name=c['name']),
                    date_week=self.week
                ))
                self.current_console_draft = None
"""

start = -1
end = -1
for i, line in enumerate(lines):
    if '# Konsolenentwicklung' in line:
        start = i
    if start != -1 and 'self.current_console_draft = None' in line:
        end = i + 1
        break

if start != -1 and end != -1:
    lines = lines[:start] + [new_block + '\n'] + lines[end:]

with codecs.open('logic.py', 'w', 'utf-8') as f:
    f.writelines(lines)
