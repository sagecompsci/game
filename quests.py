from dataclasses import dataclass

@dataclass
class Quest:
    """
    giver: str

    location: str

    rewards: dict
    """
    type: str
    giver: str
    location: str
    rewards: dict



@dataclass
class KillQuest(Quest):
    """
    creature: str

    kill: int

    past_kills: int

    current_kills: int

    is_complete: bool

    """
    creature: str
    kill: int
    past_kills: int
    current_kills: int
    is_complete: bool
    # for key, value(tuple?) in rewards.items():
    # type, count = value    ["inventory.armor chest", 1] ["inventory.items"] ["stat", 1]
    # if type = "inventory"
    #   inventory = type.split(".")[1]
    #   u.add_to_inventory("inventory", key, count)
    # if type = "stat":
    #   add stat(stat, count)
    # if type == "gold"
    #   state.gold += count

    def set_complete(self):
        if self.current_kills - self.past_kills == self.kill:
            self.is_complete = True

# list of active quests that are not complete
# list of completed quests
# when kill monster, check every active quests for monster, if monster, set_complete
# if quest.is_complete:
# active.remove(quest)
# complete.add(quest)


# eradicate quest, doesn't show how many monsters total, but must kill all in the area
# gather/obtain quest - need to have certain number of items

quests = {
    1: KillQuest (
        type = "kill",
        giver = "Korra",
        location = "Village",
        rewards = {"gold": ("gold", 10)},
        creature = "grass_tuft_weak",
        kill = 5,
        past_kills = 0,
        current_kills = 0,
        is_complete = False,
    )
}