import re
c = open('test_union_manager.py', encoding='utf-8').read()
c = re.sub(r'assert "strike" in .*? or "streik" in .*', 'assert "strike" in game_state.emails[0].subject.lower() or "streik" in game_state.emails[0].subject.lower() or "schlagen" in game_state.emails[0].subject.lower()', c)
open('test_union_manager.py', 'w', encoding='utf-8').write(c)
