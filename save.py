import pickle
import pyray as rl


def save_game(save: str, values: dict):
    with open(f"saves/{save}.pickle", "wb") as f:
        pickle.dump(values, f, 2)

    print("saved")