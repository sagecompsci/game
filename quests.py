from dataclasses import dataclass

@dataclass
class Quest:
    """
    giver: str

    location: str

    rewards: dict

    status: str - "", "accepted", "completed", "need-reward", "rewarded"
    """
    type: str
    giver: str
    location: str
    rewards: dict
    status: str



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
    kill_count: int
    # for key, value(tuple?) in rewards.items():
    # type, count = value    ["inventory.armor chest", 1] ["inventory.items"] ["stat", 1]
    # if type = "inventory"
    #   inventory = type.split(".")[1]
    #   u.add_to_inventory("inventory", key, count)
    # if type = "stat":
    #   add stat(stat, count)
    # if type == "gold"
    #   state.gold += count

    def update_kills(self, creature, count):
        if creature == self.creature:
            self.kill_count += count


    def set_complete(self):
        if self.kill_count >= self.kill:
            self.status = "completed"


# eradicate quest, doesn't show how many monsters total, but must kill all in the area
# gather/obtain quest - need to have certain number of items

# function for determining if a quest is available and if it can be added to available list
def set_available_quests(available_quests: set):
    if not 1 in available_quests:
        available_quests.add(1)


def update_quests(available_quests: set, active_quests: set, completed_quests: set, all_quests: dict) :
    accepted = set()
    for code in available_quests:
        quest = all_quests[code]
        if quest.status == "accepted":
            accepted.add(code)
    available_quests -= accepted
    active_quests.update(accepted)

    rewarded = set()
    for code in active_quests:
        quest = all_quests[code]
        if quest.status == "accepted":
            quest.set_complete()
        elif quest.status == "needs_reward":
            # give reward
            quest.status = "rewarded"
            rewarded.add(code)
    active_quests -= rewarded
    completed_quests.update(rewarded)

    return available_quests, active_quests, completed_quests


def complete_quests(active_quests: set, all_quests: dict):
    for code in active_quests:
        quest = all_quests[code]



all_quests = {
    1: KillQuest (
        type = "kill",
        giver = "Korra",
        location = "Village",
        rewards = {"gold": ("gold", 10)},
        creature = "grass_tuft_weak",
        kill = 5,
        kill_count = 0,
        status = "",
    )
}