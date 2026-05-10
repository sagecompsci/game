from templates.npc_template import write_file_npc
from classes.Dialog import Dialog
from classes.DialogInfo import DialogInfo
from classes.Npc import Npc

options = {
    "town": {
        "Tell me about the town.": 4,
        "Bye.": 0
    },
}

dialog_info = DialogInfo(
    quest_none =  1,
    quest_rewarded = 9,
    quest_accepted = 6,
    accept_dialog = 2,
    give_reward =  7,
    quest_not_complete = 8,
)

dialogs = {
    1: Dialog (
        text = "Can you help me kill some weeds?",
        options =  {
            "Yes": 2,
            "Maybe Later": 3,
        },
    ),

    2: Dialog (
        text = "Do you have any questions?",
        options = options["town"],
    ),

    3: Dialog(
        text = "Let me know if you change your mind.",
        options = options["town"],
    ),


    4: Dialog (
        text = "This is a small town, something about the chief.",
        options = {
            "Where is the chief?": 5,
            "Bye.": 0
        },
    ),

    5: Dialog(
        text = "You should be able to find him in the south field.",
        options = options["town"],
    ),


    6: Dialog (
        text = "Do you need something?",
        options =  {
            "I completed the quest.": 7
        } | options["town"],
    ),

    7: Dialog(
        text = "Thanks for your help! Here are some items.",
        options = options["town"],
    ),

    8: Dialog(
        text = "You aren't dont yet.",
        options = options["town"],
    ),

    9: Dialog(
        text = "Do you need something?",
        options = options["town"],
    ),
}


npc = Npc (
    name = "Korra",
    image = "npc",
    pos = "",
    quest_code = 1,
    dialogs = dialogs,
    dialog_info = dialog_info,
    dialog_code = 1
)

write_file_npc(1, npc)