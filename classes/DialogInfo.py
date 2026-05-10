from dataclasses import dataclass

@dataclass
class DialogInfo:
    """
    quest_none: int - default dialog if you have not accepted the quest

    quest_rewarded: int - default dialog if you have been rewarded

    quest_accepted: int - default dialog if you have accepted the quest

    accept_dialog: int - what dialog plays when you accept the quest (when this plays quests status = "accepted")

    give_reward: int - what dialog plays when you say you have completed the quest

    quest_not_complete: int - dialog that plays if you say you have completed the quest but you haven't

    """
    quest_none: int
    quest_rewarded: int
    quest_accepted: int
    accept_dialog: int
    give_reward: int
    quest_not_complete: int