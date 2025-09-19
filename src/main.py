from json import load
from os import listdir
from os.path import dirname, abspath, isfile

from corral import corral
from data import Data, Text, Item, Seed, Crop, Animal
from farmland import farmland
from other import next_day
from player import Player
from shop import buy, sell
from ui import get_choice_in_options, get_bool_input, DisplayInfo


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

    gameplay = 0
    for i in text.keys():
        if i.startswith("page_"):
            gameplay += 1

    return Data(text, items, seeds, crops, animals, language_list, gameplay)


def load_player(root_path: str, text: Text) -> Player:
    print(text["start_4"])
    while True:
        match get_choice_in_options(text["start_5"], lambda x: 0 <= x < 3, text["input_error"], text["input_not_int"]):
            case 0:
                print(text["start_7"])
                for i in listdir(f"{root_path}/archive"):
                    if i.endswith(".json"):
                        print(f"    {i[:-5]}")
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


def setting(player: Player, data: Data) -> None:
    while True:
        match get_choice_in_options(data.text["other_0"], lambda x: 0 <= x < 5, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                info = DisplayInfo(data.text["other_1"], data.text["no_item"])
                for i in data.language:
                    info.add((i, data.text[i]))
                info.display()
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


def docs(data: Data) -> None:
    while True:
        match get_choice_in_options(data.text["docs_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                while True:
                    keys = ()
                    match get_choice_in_options(data.text["docs_1"], lambda x: 0 <= x < 5, data.text["input_error"], data.text["input_not_int"]):
                        case 0:
                            keys = data.items.keys()
                        case 1:
                            keys = data.crops.keys()
                        case 2:
                            keys = data.animals.keys()
                        case 3:
                            keys = data.seeds.keys()
                        case 4:
                            break
                    info = DisplayInfo(data.text["docs_2"], data.text["no_item"])
                    for i in keys:
                        info.add((data.text[i], data.text[i + "_describe"]))
                    info.display()
            case 1:
                pages = 0
                while True:
                    print(data.text[f"page_{pages}"])
                    if pages == 0 and data.gameplay_number == 1:
                        if get_choice_in_options(data.text["docs_6"], lambda x: x == 0, data.text["input_error"], data.text["input_not_int"]) == 0:
                            break
                    elif pages == 0:
                        match get_choice_in_options(data.text["docs_3"], lambda x: 0 <= x < 2, data.text["input_error"], data.text["input_not_int"]):
                            case 0:
                                pages = 1
                            case 1:
                                break
                    elif pages > 0 and pages < data.gameplay_number - 1:
                        match get_choice_in_options(data.text["docs_4"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
                            case 0:
                                pages -= 1
                            case 1:
                                pages += 1
                            case 2:
                                break
                    elif pages == data.gameplay_number - 1:
                        match get_choice_in_options(data.text["docs_5"], lambda x: 0 <= x < 2, data.text["input_error"], data.text["input_not_int"]):
                            case 0:
                                pages -= 1
                            case 1:
                                break
            case 2:
                return


def main(player: Player, data: Data) -> None:
    print(data.text["main_0"])
    print(data.text["home_4"].format(player.day))
    while True:
        match get_choice_in_options(data.text["main_1"], lambda x: 0 <= x < 6, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                farmland(player, data)
            case 1:
                corral(player, data)
            case 2:
                while True:
                    match get_choice_in_options(data.text["main_2"], lambda x: 0 <= x < 9, data.text["input_error"], data.text["input_not_int"]):
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
                    match get_choice_in_options(data.text["home_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
                        case 0:
                            print(data.text["home_1"])
                            next_day(player, data)
                            print(data.text["home_4"].format(player.day))
                        case 1:
                            print(data.text["shop_1"].format(player.bag.money))
                            while True:
                                match get_choice_in_options(data.text["home_2"], lambda x: 0 <= x < 5, data.text["input_error"], data.text["input_not_int"]):
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
                                info = DisplayInfo(data.text["home_3"], data.text["no_item"])
                                for i, (k, v) in enumerate(bag.items()):  # type: ignore
                                    info.add((i + 1, data.text[k], v, data.text[k + "_describe"]))
                                info.display()
                        case 2:
                            break
            case 4:
                setting(player, data)
            case 5:
                docs(data)


if __name__ == "__main__":
    root_path = abspath(dirname(__file__) + "/..").replace("\\", "/")
    DATA = init(root_path, "zh-tw")
    player = load_player(root_path, DATA.text)
    DATA.update_text(f"{root_path}/language/{player.language}.json")
    main(player, DATA)
