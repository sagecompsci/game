from dataclasses import dataclass
from classes.Enum import Status

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
    status: Status
    is_complete: bool



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
            self.is_complete = True

    @classmethod
    def from_dict(cls, values):
        return cls (
            type = values["type"],
            giver = values["giver"],
            location = values["location"],
            rewards = values["rewards"],
            status = Status.available,
            is_complete = False,
            creature = values["creature"],
            kill = values["kill"],
            kill_count = 0
        )
