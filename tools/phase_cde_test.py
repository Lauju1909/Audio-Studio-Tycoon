import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic import GameState
from models import GameProject, Engine

def test_phase_c_d_e():
    print("Testing Phase C, D, E Logic...")
    state = GameState()
    state.money = 5000000

    if hasattr(state, 'build_presswerk'):
        state.build_presswerk()
        print("Built Presswerk")
        
        state.expand_storage()
        print("Expanded Storage")
        
        dummy_engine = Engine("Test Engine", [])
        proj = GameProject(name="Test Game", topic="Fantasy", genre="RPG", sliders={},
                           platform="PC", audience="Jeder", engine=dummy_engine)
        proj.state = "finished"
        proj.sales = 100
        proj.revenue = 1000
        state.game_history.append(proj)
        
        if hasattr(state, 'produce_units'):
            res = state.produce_units(0, 5000)
            print("Produce Units returned:", res)
        else:
            print("No produce_units method")
            
    if hasattr(state, 'build_server_room'):
        state.build_server_room()
        print("Built Server Room")
        
        if hasattr(state, 'expand_server_capacity'):
            state.expand_server_capacity()
            print("Expanded Server Room")
        else:
            print("No expand_server_capacity method")

    print("Phase C-E test executed successfully")

if __name__ == "__main__":
    test_phase_c_d_e()
