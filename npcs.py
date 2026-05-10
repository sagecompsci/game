# from typing import Callable
# import re
#
# import pyray as rl
#
# from dataclasses import dataclass
#
# @dataclass
# class Dialog:
#     """
#     text: str - the text npc is saying
#     options: dict[int, str] - options for what player can say
#     on_click: Callable - what function to call when player chooses an option
#     """
#     text: str
#     options: dict[int, str]
#     on_click: Callable
#
#
# # town = "Tell me about the town."
# # town_code = 4
# not_accepted_key = 1
# default_key = 2
# accepted_key = 6
#
# quest_key = 1
# quest_code = default_key
#
# completed_key = 7
# not_completed_key = 8
#
# quest_yes_key = 1
# quest_yes_text = "Yes"
# quest_yes_code = default_key
#
# quest_no_key = 2
# quest_no_text = "Maybe Later"
# quest_no_code = 3
#
# town_dialog_key = 4
# town_answer_key = 3
# town_answer_text = "Tell me about the town"
# town_answer_code = town_dialog_key
#
#
# chief_dialog_key = 5
# chief_answer_key = 6
# chief_answer_text = "Where is the chief?"
# chief_answer_code = chief_dialog_key
#
#
# end_answer_key = 4
# end_answer_text = "Bye"
# # end function that checks if completed, accepted, or not accepted
# # variable quest status str
#
# quest_options = {
#     quest_yes_key: quest_yes_text,
#     quest_no_key: quest_no_text
# }
#
# town_options = {
#     town_answer_key: town_answer_text,
#     end_answer_key: end_answer_text
# }
#
# chief_options = {
#     chief_answer_key: chief_answer_text,
#     end_answer_key: end_answer_text
# }
#
# completed_answer_key = 5
# completed_answer_text = "I completed the quest"
# completed_answer_code = 7
# not_completed_answer_code = 8
#
#
# options = {
#     "town": {
#         "town": 4,
#         "bye": 0
#     },
#     "completed": {
#         "completed the quest": (7, 8)
#     }
#
# }
#
#
# dialog = {
#     "quest_none": 1,
#     "quest_rewarded": 9,
#     "quest_accepted": 6,
#
#     "accept_quest": 2,
#     "give_reward": 7,
#     "quest_not_complete": 8,
#     1: ("give quest text", {
#         "yes": 2,
#         "later": 3
#     }),
#
#     2: ("do you have any questions",
#         options["town"]
#     ),
#
#     3: ("let me know if you change your mind",
#         options["town"]
#     ),
#
#     4: ("about the town",
#         {
#             "chief": 5,
#             "bye": 0
#         }
#         ),
#     5: ("about the chief",
#         options["town"]
#         ),
#
#     6: ("do you need something", {"completed": 7} | options["town"]),
#
#     7: ("thanks",
#         options["town"]),
#     8: ("not done yet",
#         options["town"]),
#
#     9: ("do you need something", options["town"]),
#
# }






# def quest(answer: int, quest_status: str):
#     if answer == quest_yes_key:
#         return quest_yes_code, "accepted", False
#     return quest_no_code, quest_status, False
#
# def completed(answer: int, quest_status: str) :
#     if answer == completed_answer_key:
#         if quest_status == "completed":
#             quest_status = "need_reward"
#             return completed_answer_code, quest_status, False
#
#         return not_completed_answer_code, quest_status, False
#
#     return town(answer, quest_status)
#
# def town(answer: int, quest_status: str):
#     if answer == town_answer_key:
#         return town_answer_code, quest_status, False
#     values = end(quest_status)
#     return values
#
# def chief(answer: int, quest_status):
#     if answer == chief_answer_key:
#         return chief_answer_code, quest_status, False
#     values = end(quest_status)
#     return values
#
# def end(quest_status: str):
#     if quest_status in ("accepted", "completed"):
#         return accepted_key, quest_status, True
#     if quest_status in ("need_reward", "rewarded"):
#         return default_key, quest_status, True
#
#     return not_accepted_key, quest_status, True
#
#
#
# dialogs = {
#     1: Dialog (
#         text = "Can you help me kill some weeds?",
#         options = quest_options,
#         on_click = quest,
#     ),
#     2: Dialog(
#         text = "Do you have any questions?",
#         options = town_options,
#         on_click = town,
#     ),
#     3: Dialog (
#         text = "Let me know if you change your mind.",
#         options = town_options,
#         on_click = town,
#     ),
#     4: Dialog (
#         text = "This is a small town. Something about the chief.",
#         options = chief_options,
#         on_click = chief,
#     ),
#     5: Dialog (
#         text = "You should be able to find him the south field. Anything else?",
#         options = town_options,
#         on_click = town,
#     ),
#     6: Dialog (
#         text = "Do you need something?",
#         options = {completed_answer_key: completed_answer_text} | town_options,
#         on_click = completed,
#     ),
#     7: Dialog (
#         text = "Thanks for the help! Here's some stuff",
#         options = town_options,
#         on_click = town,
#     ),
#     8 : Dialog (
#         text = "You have killed {kill_count}/{kill} of {creature}.",
#         options = town_options,
#         on_click = town,
#     ),
# }
#
#
# # npc =  Npc (
# #     name = "Korra",
# #     image = "npc",
# #     pos = "",
# #     quest_code = 1,
# #     dialogs = dialogs,
# #     dialog_code = 1,
# # )
#
# npc =  Npc (
#     name = "Korra",
#     image = "npc",
#     pos = "",
#     quest_code = 1,
#     dialogs = dialog,
#     dialog_code = 1,
# )
#
#
# # if quest has been accepted but not completed, should show num 6 dialog
# # if quest has been completed, should show number 2
# # you choose "I have completed the quest" but you have not, it should show 8. if you have completed it should show 7
#
#     # will take is_quest_complete, is_reward_given,
#     # on_click will return dialog_code, is_reward_given, items to put in inventory or gold
#     #
#     # if quest if complete, if reward is give, if quest is in active, move to completed