from collections import namedtuple

Item = namedtuple("Item", ["name", "description", "locations", "uses"])

item_data = {
    "minotaur_horn": Item(
        name="Minotaur Horn",
        description="This is a minotaur horn from a minotaur.",
        locations=["drops,Minotaur"],
        uses=["Strength Potion"],
    ),

    "living_stone": Item(
        name="Living Stone",
        description="You can feel a faint heartbeat from the stone",
        locations=["drops,Minotaur"],
        uses=["unknown"]
    )
}