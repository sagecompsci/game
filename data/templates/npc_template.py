from templates.main_template import write_file

from classes.Npc import Npc
from classes.Dialog import Dialog
from classes.DialogInfo import DialogInfo

dialog_info = DialogInfo(
    quest_none =  0,
    quest_rewarded =  0,
    quest_accepted =  0,
    accept_dialog = 0,
    give_reward =  0,
    quest_not_complete = 0,
)

dialogs = {
    1: Dialog (
        text = "Can you help me kill some weeds?",
        options =  {
            "Yes": 2,
            "Maybe Later": 3,
        },
    ),
}

npc = Npc (
    name = "",
    image = "npc",
    pos = "",
    quest_code = 1,
    dialogs = dialogs,
    dialog_info = dialog_info,
    dialog_code = 1
)

def write_file_npc(key: str | int, npc: Npc):
    file = f"../{key}.json"
    write_file(file, npc.to_dict())