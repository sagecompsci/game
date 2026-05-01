from collections import namedtuple

Item = namedtuple("Item", ["name", "description", "type", "locations", "uses"])

item_data = {
    "grass": Item(
        name = "Grass Tuft",
        description = "This grass is tougher than normal. Maybe you could make something with it.",
        type = "items",
        locations = ["drops,grass_tuft"],
        uses = ["craft armor"],

    ),
    "minotaur_horn": Item(
        name="Minotaur Horn",
        description="This is a minotaur horn from a minotaur.",
        type = "items",
        locations=["drops,Minotaur"],
        uses=["Strength Potion"],
    ),

    "living_stone": Item(
        name="Living Stone",
        description="You can feel a faint hearbeat from the stone",
        type = "items",
        locations=["drops,Minotaur"],
        uses=["unknown"],
    )
}