from utilities.get_data import get_item

# def edit_inventory(inventory: dict, item: str, type: str, count: int, equips: bool = False):
#     if type == "gold":
#         edit_dict(inventory, type, count, type)
#
#     else:
#         if equips:
#             key = "equips"
#         else:
#             keys = ["weapons", "armor", "accessories", "items", "consumables", "special"]
#             for inv_key in keys:
#                 if inv_key in type:
#                     key = inv_key
#         edit_dict(inventory[key], item, count, type)



def edit_dict(dictionary: dict, item_key: str, count: int):
    try:
        new_count = count
        if item_key in dictionary.keys():
            new_count = dictionary[item_key] + count

        if new_count > 0:
            dictionary[item_key] = new_count
        elif new_count == 0:
            dictionary.pop(item_key)
        else:
            raise Exception("Item count cannot be negative")

    except Exception as e:
        print(e)


def edit_inventory(inventory: dict, item_key: str, count: int, equips: bool = False):
    item = get_item(item_key)
    inv_key = item["inventory"]

    if equips:
        edit_dict(inventory["equips"], item_key, count)
        edit_dict(inventory[inv_key], item_key, -count)

    else:
        edit_dict(inventory[inv_key], item_key, count)


