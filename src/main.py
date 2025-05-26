from json import load
from os.path import dirname, abspath, isfile
from typing import Literal

from data import *
from player import *
from ui import *
from other import *


def init(root_path: str, language: str) -> Data:
    try:
        with open(f"{root_path}/language/{language}.json", "r", encoding="utf-8") as f:
            text = Text(load(f))
    except Exception as e:
        print("Error: Unable to load language file. error: ", e)
        exit(1)

    try:
        with open(f"{root_path}/data/items.json", "r", encoding="utf-8") as f:
            items = {k: Item(k, v["sell_price"]) for k, v in load(f).items()}
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/items.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("items", e))
        exit(1)

    try:
        with open(f"{root_path}/data/seeds.json", "r", encoding="utf-8") as f:
            seeds = {k: Seed(k, v["sell_price"]) for k, v in load(f).items()}
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/seeds.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("seeds", e))
        exit(1)

    try:
        with open(f"{root_path}/data/crops.json", "r", encoding="utf-8") as f:
            crops = {k: Crop(v["growth_time"], v["sell_price"], v["soil_needed"], v["pest_resistance"]) for k, v in load(f).items()}
    except FileNotFoundError | IOError as e:
        print(text["file_error"].format(f"{root_path}/data/crops.json", e))
        exit(1)
    except Exception as e:
        print(text["load_data_error"].format("crops", e))
        exit(1)

    try:
        with open(f"{root_path}/data/animals.json", "r", encoding="utf-8") as f:
            animals = {
                k: Animal(
                    v["baby_price"],
                    v["growth_time"],
                    v["sell_price"],
                    tuple(v["food"]),
                    v["food_needed_per_day"],
                    v["required_neatness"],
                )
                for k, v in load(f).items()
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
        match get_choice_in_options(text["start_5"], lambda x: 0 <= x < 3, text["input_error"], text["input_not_int"]):
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
        match get_choice_in_options(data.text["farm_op_0"], lambda x: 0 <= x < 7, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                m: dict[int, str] = {}
                info = Display_info(data.text["farm_op_12"], data.text["no_item"])
                for i, (k, v) in enumerate(player.bag.seeds.items()):
                    info.add((i + 1, data.text[k], v))
                    m[i] = k
                print(data.text["farm_op_1"])
                info.display()
                choice_seed = get_int_input(
                    data.text["farm_op_2"], lambda x: 0 <= x < len(m), data.text["farm_op_3"], data.text["input_not_int"]
                )
                if choice_seed == -1:
                    continue
                if player.bag.seeds[m[choice_seed]] < len(choices):
                    print(data.text["farm_op_7"].format(data.text[m[choice_seed]]))
                    continue
                plant(player, choices, m[choice_seed])
            case 1:
                print(data.text["farm_op_5"].format(data.text["organic_fertilizer"], player.bag.items["organic_fertilizer"]))
                print(data.text["farm_op_5"].format(data.text["chemical_fertilizer"], player.bag.items["chemical_fertilizer"]))
                choice_fertilizer = get_choice_in_options(
                    data.text["farm_op_6"], lambda x: 0 <= x < 3, data.text["farm_op_3"], data.text["input_not_int"]
                )
                if choice_fertilizer == 2:
                    continue
                if choice_fertilizer == 0:
                    choice_fertilizer = "organic_fertilizer"
                else:
                    choice_fertilizer = "chemical_fertilizer"
                if player.bag.items[choice_fertilizer] < len(choices):
                    print(data.text["farm_op_7"].format(data.text[choice_fertilizer]))
                    continue
                fertilize(player, choices, choice_fertilizer == "organic_fertilizer")
            case 2:
                if not get_bool_input(data.text["farm_op_8"], False):
                    continue
                crops = harvest_remove(player, choices)
                print(data.text["farm_op_9"])
                info = Display_info(data.text["farm_op_13"], data.text["no_item"])
                for k, v in crops.items():
                    info.add((data.text[k], v))
                    player.bag.crops[k] += v
                info.display()
            case 3:
                print(data.text["farm_op_5"].format(data.text["herbicide"], player.bag.items["herbicide"]))
                choice_herbicide = get_choice_in_options(
                    data.text["farm_op_11"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]
                )
                if choice_herbicide == 2:
                    continue
                if choice_herbicide == 0 and player.bag.items["herbicide"] < len(choices):
                    print(data.text["farm_op_7"].format(data.text["herbicide"]))
                    continue
                weed(player, choices, choice_herbicide == 0)
            case 4:
                print(data.text["farm_op_5"].format(data.text["insecticide"], player.bag.items["insecticide"]))
                choice_insecticide = get_choice_in_options(
                    data.text["farm_op_10"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]
                )
                if choice_insecticide == 2:
                    continue
                if choice_insecticide == 0 and player.bag.items["insecticide"] < len(choices):
                    print(data.text["farm_op_7"].format(data.text["insecticide"]))
                    continue
                disinfestation(player, choices, choice_insecticide == 0)
            case 5:
                info = Display_info(data.text["farmland_info"], data.text["no_item"])
                for i in choices:
                    j = player.farmland[i]
                    info.add(
                        (
                            i + 1,
                            data.text[j.crop] if j.crop != "" else data.text["empty"],
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
        match get_choice_in_options(data.text["farmland_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                choices = get_range_input(
                    data.text["farmland_1"],
                    lambda x: 0 <= x < player.farmland_size,
                    data.text["farmland_2"],
                    data.text["input_not_int"],
                    data.text["format_error"],
                )
                if choices == (-1,):
                    continue
                elif choices == (-2,):
                    choices = tuple(range(player.farmland_size))
                manage_farmland(player, data, choices)
            case 1:
                info = Display_info(data.text["farmland_info"], data.text["no_item"])
                for i in range(player.farmland_size):
                    j = player.farmland[i]
                    info.add(
                        (
                            i + 1,
                            data.text[j.crop] if j.crop != "" else data.text["empty"],
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
        match get_choice_in_options(data.text["corral_op_0"], lambda x: 0 <= x < 7, data.text["input_error"], data.text["input_not_int"]):
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
        match get_choice_in_options(data.text["corral_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                choices = get_range_input(
                    data.text["corral_1"],
                    lambda x: 0 <= x < player.corral_size,
                    data.text["corral_2"],
                    data.text["input_not_int"],
                    data.text["format_error"],
                )
                if choices == (-1,):
                    continue
                elif choices == (-2,):
                    choices = tuple(range(player.corral_size))
                manage_corral(player, data, choices)
            case 1:
                info = Display_info(data.text["corral_info"], data.text["no_item"])
                for i in range(player.corral_size):
                    j = player.corral[i]
                    info.add(
                        (
                            i + 1,
                            data.text[j.animal] if j.animal != "" else data.text["empty"],
                            j.growth_time,
                            j.hunger,
                            j.neatness,
                            j.health,
                            j.sick_prob,
                            j.sick,
                            j.grow_up,
                        )
                    )
                print(data.text["corral_3"].format(player.corral_size))
                info.display()
            case 2:
                return


def buy(player: Player, data: Data, kind: Literal["seeds", "items", "crops", "animals"]) -> None:
    match kind:
        case "seeds":
            bag = player.bag.seeds
            now_data = data.seeds
        case "items":
            bag = player.bag.items
            now_data = data.items
        case "crops":
            bag = player.bag.crops
            now_data = data.crops
        case "animals":
            bag = player.bag.animals
            now_data = data.animals
    while True:
        info = Display_info(data.text["shop_0"], data.text["no_item"])
        d: dict[int, str] = {}
        for i, (k, v) in enumerate(now_data.items()):
            info.add((i + 1, data.text[k], int(limit_range(v.sell_price, "*", 1.2, 1, float("inf"), 0))))
            d[i] = k
        print(data.text["shop_1"].format(player.bag.money))
        print(data.text["shop_7"])
        info.display()
        result = get_int_input(data.text["shop_8"], lambda x: 0 <= x < len(now_data), data.text["input_error"], data.text["input_not_int"])
        if result == -1:
            return
        choice = d[result]
        buy_price = int(limit_range(now_data[choice].sell_price, "*", 1.2, 1, float("inf"), 0))
        buy_number = 1 + get_int_input(
            data.text["shop_9"],
            lambda x: 0 <= x < player.bag.money // buy_price,
            data.text["shop_10"],
            data.text["input_not_int"],
        )
        if buy_number <= 0:
            return
        bag[choice] = bag[choice] + buy_number
        player.bag.money -= buy_number * buy_price
        print(data.text["shop_11"].format(buy_number, data.text[choice], buy_price * buy_number))


def sell(player: Player, data: Data, kind: Literal["seeds", "items", "crops", "animals"]) -> None:
    match kind:
        case "seeds":
            bag = player.bag.seeds
            now_data = data.seeds
        case "items":
            bag = player.bag.items
            now_data = data.items
        case "crops":
            bag = player.bag.crops
            now_data = data.crops
        case "animals":
            bag = player.bag.animals
            now_data = data.animals
    while True:
        info = Display_info(data.text["shop_0"], data.text["no_item"])
        d: dict[int, str] = {}
        for i, (k, v) in enumerate(bag.items()):
            info.add((i + 1, data.text[k], now_data[k].sell_price, v))
            d[i] = k
        print(data.text["shop_1"].format(player.bag.money))
        print(data.text["shop_2"])
        info.display()
        result = get_int_input(data.text["shop_3"], lambda x: 0 <= x < len(bag), data.text["input_error"], data.text["input_not_int"])
        if result == -1:
            return
        choice = d[result]
        sell_number = 1 + get_int_input(
            data.text["shop_4"], lambda x: 0 <= x < bag[choice], data.text["shop_5"], data.text["input_not_int"]
        )
        if sell_number <= 0:
            return
        bag[choice] -= sell_number
        player.bag.money += sell_number * now_data[choice].sell_price
        print(data.text["shop_6"].format(sell_number, data.text[choice], now_data[choice].sell_price * sell_number))


def setting(player: Player, data: Data) -> None:
    while True:
        match get_choice_in_options(data.text["other_0"], lambda x: 0 <= x < 5, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                print(data.text["other_1"])
                for i in data.language:
                    print("    " + i)
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
                    result = get_bool_input(data.text["other_8"], False)
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
                print(data.text["other_10"].format(player.name))
                player.name = input(data.text["other_9"])
                print(data.text["other_11"].format(player.name))
            case 3:
                if get_bool_input(data.text["other_5"], False):
                    print(data.text["game_close"])
                    exit()
            case 4:
                return


def main(player: Player, data: Data) -> None:
    print(data.text["main_0"])
    print(data.text["home_4"].format(player.day))
    while True:
        match get_choice_in_options(data.text["main_1"], lambda x: 0 <= x < 5, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                farmland(player, data)
            case 1:
                corral(player, data)
            case 2:
                while True:
                    match get_choice_in_options(
                        data.text["main_2"], lambda x: 0 <= x < 9, data.text["input_error"], data.text["input_not_int"]
                    ):
                        case 0:
                            buy(player, data, "seeds")
                        case 1:
                            buy(player, data, "items")
                        case 2:
                            buy(player, data, "crops")
                        case 3:
                            buy(player, data, "animals")
                        case 4:
                            sell(player, data, "seeds")
                        case 5:
                            sell(player, data, "items")
                        case 6:
                            sell(player, data, "crops")
                        case 7:
                            sell(player, data, "animals")
                        case 8:
                            break
            case 3:
                while True:
                    match get_choice_in_options(
                        data.text["home_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]
                    ):
                        case 0:
                            print(data.text["home_1"])
                            next_day(player, data)
                            print(data.text["home_4"].format(player.day))
                        case 1:
                            print(data.text["shop_1"].format(player.bag.money))
                            while True:
                                match get_choice_in_options(
                                    data.text["home_2"], lambda x: 0 <= x < 5, data.text["input_error"], data.text["input_not_int"]
                                ):
                                    case 0:
                                        bag = player.bag.seeds
                                    case 1:
                                        bag = player.bag.items
                                    case 2:
                                        bag = player.bag.crops
                                    case 3:
                                        bag = player.bag.animals
                                    case 4:
                                        break
                                info = Display_info(data.text["home_3"], data.text["no_item"])
                                for i, (k, v) in enumerate(bag.items()):  # type: ignore
                                    info.add((i + 1, data.text[k], v, data.text[k + "_describe"]))
                                info.display()
                        case 2:
                            break
            case 4:
                setting(player, data)


if __name__ == "__main__":
    root_path = abspath(dirname(__file__) + "/..").replace("\\", "/")
    DATA = init(root_path, "zh-tw")
    player = load_player(root_path, DATA.text)
    DATA.update_text(f"{root_path}/language/{player.language}.json")
    main(player, DATA)
