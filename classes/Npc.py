from dataclasses import dataclass
from classes.Dialog import Dialog
from classes.DialogInfo import DialogInfo

@dataclass
class Npc:
    """
    name: str - name of npc

    image: str - name of image file

    pos: str - position of npc

    quest_code: int - key of quest

    dialogs: dict[int, Dialog] - dictionary of all dialogs {1: "text", "options": {"yes": 1}}

    quest_status: str - "", "accepted", "completed", "need_reward", "rewarded"

    dialog_code: int - key for current dialog

    """
    name: str
    image: str
    pos: str
    quest_code: int
    dialogs: dict[int, Dialog]
    dialog_info: DialogInfo
    dialog_code: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "image": self.image,
            "pos": self.pos,
            "quest_code": self.quest_code,
            "dialogs": dict([(code, dialog.__dict__) for code, dialog in self.dialogs.items()]) ,
            "dialog_info": self.dialog_info.__dict__,
            "dialog_code": self.dialog_code,
        }

    @classmethod
    def from_dict(cls, values: dict):
        return cls(
            name = values["name"],
            image = values["image"],
            pos = values["pos"],
            quest_code = values["quest_code"],
            dialogs = dict([int(code), Dialog(**dialog)] for code, dialog in values["dialogs"].items()),
            dialog_info = DialogInfo(**values["dialog_info"]),
            dialog_code = values["dialog_code"],
        )