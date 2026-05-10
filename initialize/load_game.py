from classes.GameState import GameState
import pickle


def load_game(state: GameState) -> GameState:
    with open(f"saves/{state.save}.pickle", "rb") as f:
        values = pickle.load(f)

    state.from_dict(values)

    return state