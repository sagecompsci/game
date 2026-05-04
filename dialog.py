import pyray as rl
from django.conf.locale.ar.formats import THOUSAND_SEPARATOR

from dataclasses import dataclass

@dataclass
class NPC:
    name: str # Korra npc name to display on quest and text box
    image: str # npc file name of texture
    pos: str # key of tile they are standing on
    quest_code: int # key to the quest in dictionary and active quest list
    rewarded: bool # if player have received quest reward
    dialog: dict[int, tuple]


npc = NPC (
    name = "Korra",
    image = "npc",
    pos = "0.0,0.0",
    quest_code = 1,
    rewarded = False,
    dialog = {
        1: ("Can you help me kill some weeds?", ["Yes", "Maybe Later"], [2, 3]),
        2: ("Do you have any questions?", ["Tell me about the town.", "No"], [4, 0], quest_code),
        4: ("This is a small town. Something about the chief.", ["Where is the chief?", "Bye"], [5, 0]),
        5: ("You should be able to find him in the south field. Anything else?", ["Tell me About the town.", "No"], [4, 0]),
        3: ("Let me know if you change your mind.", ["Tell me about the town.", "Bye"], [4, 0])
    }
)

display dialog:
    text = dialog[key][0]
    answers = dialog[key][1]
    new_index = dialog[key][2]
    if dialog[key][3]:
        quest_index = dialog[key][3]

"""
Can you help kill some weeds?
    - Yes
        Do you have any questions?
            - Tell me about the town
                Town description. Any other questions?
                    - Where is the cheif?
                        He's usually in location at this time of day. Anything else?
                            - Tell me about the town
                            - No ## 
                    - No ## 
            - No  ## something that marks that this ends the conversation
        
    - Maybe Later
        Let me know if you ever change your mind.
            - Tell me about the town
            - bye ## 


"""



["I have a quest. Do you want it?"]

answer = ["yes", "maybe later"]

if answer == 1:
    create quest
    ["response dialog 1"]

if answer == 2:
    ["response dialog 2"]

quest complete dialog

dialog is a dict
dialog = {
    1: ("Thanks for completing the quest, here's your reward"),
    0: ("What's taking so long, do you need something", ["tell me about the quest", "no"], [3, 6]),
    2: ("this is the dialog", ["answer 1", "answer 2", "answer 3"], [3, 4, 5]),
    3: ("this is the answer 1 dialog"),
    4: ("this is the answer 2 dialog"),
    5: ("this is the answer 3 dialog"),
}
"""
current_text is an index
if state.menu == "talking":
    rl.draw_texture_ex("large_text_box")
    rl.draw_text_ex(current_text)

when click on person to talk sets current dialog

create npc dataclass
npc keeps track of current dialog
when close text, it sets the dialog for the next time

draw npc in the house
put in list of npcs
if standing next to npc and right click on them:
    open text box with their name
    display current dialog
    display answer options, to close text box need to answer [bye]
    answer options take a second to display to prevent accidental double clicking

    if click on text box

    if active quest from npc display certain option
    if completed quest from npc and not given reward display ["I completed the quest"]
        then should give reward, then update npc 
    
    when completed quest is moved to complted list, should update npc

list of active quests
each npc also needs to know what quest they have

quest info should be in a file that has a dictionary of quests and their data. npc quest list is list of keys. when they
give a quest, the info is retrieved from the dictionary and Quest object is created and put into active quest list

Quest object has a key. When you click on on npc it checks if you have an active or completed quest with the same key as the one they
assigned. when they give reward

npc quests is a dict of keys to the quest and a true or false of whether they gave reward


"""