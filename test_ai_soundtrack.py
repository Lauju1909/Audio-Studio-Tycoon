import random
from models import GameProject
from logic import GameState

def test_ai_soundtrack():
    state = GameState()
    state.money = 1000000
    state.unlocked_technologies.append("KI-Soundtrack Generation")
    
    project = GameProject(
        name="AI Music Test",
        topic="Fantasy",
        genre="RPG",
        platform="PC",
        audience="Jeder",
        size="Klein",
        marketing="Kein Marketing"
    )
    
    ap = {"project": project, "progress": 0, "total_weeks": 10, "stage": 3, "bugs": 0}
    state.active_projects.append(ap)
    
    # Use AI soundtrack
    success = state.use_ai_soundtrack(0)
    assert success
    assert project.used_ai_soundtrack
    
    # Test scoring effect (force random to check)
    random.seed(42) # Should give > 0.4
    state.finalize_game(ap)
    
    game = state.game_history[-1]
    assert getattr(game, "used_ai_soundtrack", False)
