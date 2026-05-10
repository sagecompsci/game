journal = {
    "weed_weak": {
        "status": "seen",
        # means you have engaged in combat
        # shows name and picture and location
        "kills": 0,
    },
    "weed": {
        "status": "killed",
        # means you have killed one
        # shows stats
        "kills": 1,
    },
    "weed_strong": {
        "status": "not_seen",
        # shows ??? for everything
        "kills": 0,
    }
}

folder = "set"

levels = ["_weak", "", "_strong", "_king"]
pages = {}
page = 1

# should only show creatures for 1 level, then when you go down to the next level new creatures are added
for creature in folder:
    for level in levels:
        key = creature + level
        journal[key] = {
            "status": "not_seen",
            "kills": 0,
        }
        pages[page] = key
        page += 1


# create a dict of pages and what monster is on each page

# if on home page
for page, creature in pages.items():
    print(f"{page}. {creature}")
    # when you click on name it takes you to the page

# displays page
# if page is even:
#   page -= 1
# if page is odd:
#   creature1 = pages[page]
#   creature2 = pages[page + 1]

# if use arrows to increase/decrease, page num changes by 2
