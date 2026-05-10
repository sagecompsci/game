from utilities import files
from classes.Quest import KillQuest, Quest
from classes.Npc import Npc

def get_item(item: str) -> dict:
    path = files.read_file("data/inventory_paths.json")[item]
    return files.read_file(path)

def get_creature(creature: str) -> dict:
    path = files.read_file("data/creature_path.json")[creature]
    return files.read_file(path)

def get_npc(code: int) -> Npc:
    path = f"data/npcs/{code}.json"
    return Npc.from_dict(files.read_file(path))

def get_quest(code: int) -> Quest:
    path = f"data/quests/{code}.json"
    data = files.read_file(path)
    if data["type"] == "kill":
        return KillQuest.from_dict(data)
    else:
        return Quest(**data)


