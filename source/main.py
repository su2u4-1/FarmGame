from json import load
from os.path import dirname, abspath, isfile

from data import *
from player import *
from ui import *


def init(root_path: str, language: str) -> Data:
    with open(f"{root_path}/language/{language}.json", "r", encoding="utf-8") as f:
        text = Text(load(f))
    with open(f"{root_path}/data/items.json", "r", encoding="utf-8") as f:
        items = {k: Item(k) for k, _ in load(f).items()}
    with open(f"{root_path}/data/seeds.json", "r", encoding="utf-8") as f:
        seeds = {k: Seed(k) for k, _ in load(f).items()}
    with open(f"{root_path}/data/crops.json", "r", encoding="utf-8") as f:
        crops = {k: Crop(v["growth_time"], v["seed_price"], v["sell_price"], v["soil_needed"], v["pest_resistance"]) for k, v in load(f).items()}
    with open(f"{root_path}/data/animals.json", "r", encoding="utf-8") as f:
        animals = {
            k: Animal(v["baby_price"], v["growth_time"], v["adult_sell_price"], tuple(v["food"]), v["food_needed_per_day"], v["required_neatness"]) for k, v in load(f).items()
        }
    with open(f"{root_path}/data/language.json", "r", encoding="utf-8") as f:
        language = load(f)
    return Data(text, items, seeds, crops, animals, language)


def load_player(root_path: str, text: Text) -> Player:
    print(text["start_4"])
    while True:
        match display_option_and_get_input(text["start_5"].split("|"), lambda x: 0 <= x < 3, text["input_error"], text["input_not_int"]):
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


def manage_farmland(player: Player, data: Data) -> None:
    pass


def manage_corral(player: Player, data: Data) -> None:
    pass


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
                manage_farmland(player, data)
            case 1:
                manage_corral(player, data)
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
    main(player, DATA)
