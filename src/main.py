from json import load
from os.path import dirname, abspath, isfile
from random import randint as ri

from data import *
from player import *
from tools import limit_range
from ui import *


def init(root_path: str, language: str) -> Data:
    try:
        with open(f"{root_path}/language/{language}.json", "r", encoding="utf-8") as f:
            text = Text(load(f))
    except Exception as e:
        print("Error: Unable to load language file. error: ", e)
        exit(1)

    try:
        with open(f"{root_path}/data/items.json", "r", encoding="utf-8") as f:
            items = {k: Item(k) for k, _ in load(f).items()}
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/items.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("items", e))
        exit(1)

    try:
        with open(f"{root_path}/data/seeds.json", "r", encoding="utf-8") as f:
            seeds = {k: Seed(k) for k, _ in load(f).items()}
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/seeds.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("seeds", e))
        exit(1)

    try:
        with open(f"{root_path}/data/crops.json", "r", encoding="utf-8") as f:
            crops = {k: Crop(v["growth_time"], v["seed_price"], v["sell_price"], v["soil_needed"], v["pest_resistance"]) for k, v in load(f).items()}
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/crops.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("crops", e))
        exit(1)

    try:
        with open(f"{root_path}/data/animals.json", "r", encoding="utf-8") as f:
            animals = {
                k: Animal(v["baby_price"], v["growth_time"], v["adult_sell_price"], tuple(v["food"]), v["food_needed_per_day"], v["required_neatness"]) for k, v in load(f).items()
            }
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/animals.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("animals", e))
        exit(1)

    try:
        with open(f"{root_path}/data/language.json", "r", encoding="utf-8") as f:
            language_list = load(f)
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/language.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("language_list", e))
        exit(1)

    return Data(text, items, seeds, crops, animals, language_list)


def load_player(root_path: str, text: Text) -> Player:
    print(text["start_4"])
    while True:
        match display_option_and_get_input(text["start_5"], lambda x: 0 <= x < 3, text["input_error"], text["input_not_int"]):
            case 0:
                f = True
                while True:
                    name = input(text["start_0"])
                    if name == "-1":
                        f = False
                        break
                    elif isfile(f"{root_path}/archive/{name}.json"):
                        break
                    else:
                        print(text["start_1"].format(name))
                if f:
                    player = Player()
                    state = player.load(f"{root_path}/archive/{name}.json")
                    if state == 0:
                        print(text["start_2"].format(name))
                        return player
                    else:
                        print(text["start_6"].format(name))
            case 1:
                name = input(text["start_3"])
                if name == "-1":
                    continue
                player = Player()
                player.name = name
                return player
            case 2:
                print(text["game_close"])
                exit()


def manage_farmland(player: Player, data: Data, choices: tuple[int, ...]) -> None:
    while True:
        match display_option_and_get_input(data.text["farm_op_0"], lambda x: 0 <= x < 7, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                m: dict[int, str] = {}
                info = Display_info(data.text["farm_op_12"])
                for i, (k, v) in enumerate(player.bag.seeds.items()):
                    info.add((i + 1, data.text[k], v))
                    m[i] = k
                print(data.text["farm_op_1"])
                info.display()
                choice_seed = display_request_and_get_int_input(data.text["farm_op_2"], lambda x: 0 <= x < len(m), data.text["farm_op_3"], data.text["input_not_int"])
                if choice_seed == -1:
                    continue
                if player.bag.seeds.get(m[choice_seed], 0) < len(choices):
                    print(data.text["farm_op_7"].format(data.text[m[choice_seed]]))
                    continue
                player.bag.seeds[m[choice_seed]] -= len(choices)
                for i in choices:
                    player.farmland[i].crop = m[choice_seed]
            case 1:
                print(data.text["farm_op_5"].format(data.text["organic_fertilizer"], player.bag.items.get("organic_fertilizer", 0)))
                print(data.text["farm_op_5"].format(data.text["chemical_fertilizer"], player.bag.items.get("chemical_fertilizer", 0)))
                choice_fertilizer = display_option_and_get_input(data.text["farm_op_6"], lambda x: 0 <= x < 3, data.text["farm_op_3"], data.text["input_not_int"])
                if choice_fertilizer == 2:
                    continue
                if choice_fertilizer == 0:
                    choice_fertilizer = "organic_fertilizer"
                else:
                    choice_fertilizer = "chemical_fertilizer"
                if player.bag.items.get(choice_fertilizer, 0) < len(choices):
                    print(data.text["farm_op_7"].format(data.text[choice_fertilizer]))
                    continue
                player.bag.items[choice_fertilizer] -= len(choices)
                for i in choices:
                    player.farmland[i].soil_fertility += 1
                    if choice_fertilizer == "chemical_fertilizer":
                        player.farmland[i].organic = False
                    else:
                        player.farmland[i].bug_appear_prob += 0.05
            case 2:
                if not display_request_and_get_bool_input(data.text["farm_op_8"], False):
                    continue
                crops: dict[str, int] = {}
                for i in choices:
                    i = player.farmland[i]
                    if i.crop != "":
                        i.bug_appear_prob = limit_range(i.bug_appear_prob, False, ri(150, 250) / 100)
                        i.bug_number = 0
                        i.weed_appear_prob = limit_range(i.weed_appear_prob, False, ri(150, 250) / 100)
                        i.weed_appear = False
                        i.growth_time = 0
                        if i.ripe:
                            crop_name = i.crop.removesuffix("_seed")
                            crops[crop_name] = crops.get(crop_name, 0) + 1
                        else:
                            i.soil_fertility = int(limit_range(i.soil_fertility, True, ri(100, 150) / 100, 1, 50, None))
                        i.ripe = False
                        i.crop = ""
                print(data.text["farm_op_9"])
                for k, v in crops.items():
                    print("    " + data.text[k] + f"*{v}" if v > 1 else "")
                player.bag.crops.update(crops)
            case 3:
                print(data.text["farm_op_5"].format(data.text["herbicide"], player.bag.items.get("herbicide", 0)))
                choice_herbicide = display_option_and_get_input(data.text["farm_op_11"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"])
                if choice_herbicide == 2:
                    continue
                if choice_herbicide == 0 and player.bag.items.get("herbicide", 0) < len(choices):
                    print(data.text["farm_op_7"].format(data.text["herbicide"]))
                    continue
                if choice_herbicide == 0:
                    player.bag.items["herbicide"] -= len(choices)
                    for i in choices:
                        i = player.farmland[i]
                        i.weed_appear_prob = limit_range(i.weed_appear_prob, False, ri(200, 300) / 100)
                        i.weed_appear = False
                        i.organic = False
                else:
                    for i in choices:
                        i = player.farmland[i]
                        i.weed_appear_prob = limit_range(i.weed_appear_prob, False, ri(150, 250) / 100)
                        i.weed_appear = False
            case 4:
                print(data.text["farm_op_5"].format(data.text["insecticide"], player.bag.items.get("insecticide", 0)))
                choice_insecticide = display_option_and_get_input(data.text["farm_op_10"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"])
                if choice_insecticide == 2:
                    continue
                if choice_insecticide == 0 and player.bag.items.get("insecticide", 0) < len(choices):
                    print(data.text["farm_op_7"].format(data.text["insecticide"]))
                    continue
                if choice_insecticide == 0:
                    player.bag.items["insecticide"] -= len(choices)
                    for i in choices:
                        i = player.farmland[i]
                        i.bug_appear_prob = limit_range(i.bug_appear_prob, False, ri(200, 300) / 100)
                        i.bug_number = ri(0, i.bug_number // 10)
                        i.organic = False
                else:
                    for i in choices:
                        i = player.farmland[i]
                        i.bug_appear_prob = limit_range(i.bug_appear_prob, False, ri(150, 250) / 100)
                        i.bug_number = ri(0, i.bug_number // 5)
            case 5:
                info = Display_info(data.text["farmland_info"])
                for i in choices:
                    j = player.farmland[i]
                    info.add(
                        (
                            i + 1,
                            j.crop if j.crop != "" else data.text["empty"],
                            j.growth_time,
                            j.soil_fertility,
                            j.bug_appear_prob,
                            j.bug_number,
                            j.weed_appear_prob,
                            j.weed_appear,
                            j.ripe,
                            j.organic,
                        )
                    )
                print(data.text["farmland_3"].format(len(choices)))
                info.display()
            case 6:
                return


def farmland(player: Player, data: Data) -> None:
    while True:
        match display_option_and_get_input(data.text["farmland_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                choices = display_request_and_get_range_input(
                    data.text["farmland_1"], lambda x: 0 <= x < player.farmland_size, data.text["farmland_2"], data.text["input_not_int"], data.text["format_error"]
                )
                if choices == (-1,):
                    continue
                elif choices == (-2,):
                    choices = tuple(range(player.farmland_size))
                manage_farmland(player, data, choices)
            case 1:
                info = Display_info(data.text["farmland_info"])
                for i in range(player.farmland_size):
                    j = player.farmland[i]
                    info.add(
                        (
                            i + 1,
                            j.crop if j.crop != "" else data.text["empty"],
                            j.growth_time,
                            j.soil_fertility,
                            j.bug_appear_prob,
                            j.bug_number,
                            j.weed_appear_prob,
                            j.weed_appear,
                            j.ripe,
                            j.organic,
                        )
                    )
                print(data.text["farmland_3"].format(player.farmland_size))
                info.display()
            case 2:
                return


def manage_corral(player: Player, data: Data, choices: tuple[int, ...]) -> None:
    while True:
        match display_option_and_get_input(data.text["corral_op_0"], lambda x: 0 <= x < 7, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                pass
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                return


def corral(player: Player, data: Data) -> None:
    while True:
        match display_option_and_get_input(data.text["corral_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                choices = display_request_and_get_range_input(
                    data.text["corral_1"], lambda x: 0 <= x < player.corral_size, data.text["corral_2"], data.text["input_not_int"], data.text["format_error"]
                )
                if choices == (-1,):
                    continue
                elif choices == (-2,):
                    choices = tuple(range(player.corral_size))
                manage_corral(player, data, choices)
            case 1:
                info = Display_info(data.text["corral_info"])
                for i in range(player.corral_size):
                    j = player.corral[i]
                    info.add((i + 1, j.animal if j.animal != "" else data.text["empty"], j.growth_time, j.hunger, j.neatness, j.health, j.sick_prob, j.sick, j.grow_up))
                print(data.text["corral_3"].format(player.corral_size))
                info.display()
            case 2:
                return


def shop(player: Player, data: Data) -> None:
    pass


def next_day(player: Player, data: Data) -> None:
    pass


def setting(player: Player, data: Data) -> None:
    while True:
        match display_option_and_get_input(data.text["other_0"], lambda x: 0 <= x < 4, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                print(data.text["other_1"])
                for i in data.language:
                    print(i)
                while True:
                    choice = input(data.text["other_2"])
                    if choice not in data.language:
                        print(data.text["other_7"])
                    else:
                        player.language = choice
                        data.update_text(f"{root_path}/language/{choice}.json")
                        return
            case 1:
                if isfile(f"{root_path}/archive/{player.name}.json"):
                    result = display_request_and_get_bool_input(data.text["other_8"], False)
                else:
                    result = True
                if result:
                    try:
                        with open(f"{root_path}/archive/{player.name}.json", "w") as f:
                            f.write(player.save())
                    except FileNotFoundError | IOError:
                        print(data.text["other_4"].format(player.name))
                        continue
                    print(data.text["other_3"].format(player.name))
                    return
            case 2:
                if display_request_and_get_bool_input(data.text["other_5"], False):
                    print(data.text["game_close"])
                    exit()
            case 3:
                return


def main(player: Player, data: Data) -> None:
    print(data.text["main_0"])
    while True:
        match display_option_and_get_input(data.text["main_1"], lambda x: 0 <= x < 5, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                farmland(player, data)
            case 1:
                corral(player, data)
            case 2:
                shop(player, data)
            case 3:
                next_day(player, data)
            case 4:
                setting(player, data)


if __name__ == "__main__":
    root_path = abspath(dirname(__file__) + "/..").replace("\\", "/")
    DATA = init(root_path, "zh-tw")
    player = load_player(root_path, DATA.text)
    DATA.update_text(f"{root_path}/language/{player.language}.json")
    main(player, DATA)
