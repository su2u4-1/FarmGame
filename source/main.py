import os.path
import json5
import random
from classlib import *


N = dict[str : dict[str : int | list[str]]]
TEXT: My_dict[str:str]
DATA: dict[str : N | list[str]]
CROPS: N
ANIMALS: N


def start() -> None:
    def open_archive() -> Player:
        name = input(TEXT["start_0"])
        if name == "-1":
            return None
        path = os.path.join(root, "archive", name) + ".json5"
        if not os.path.isfile(path):
            print(TEXT["start_1"].format(name))
            return open_archive()
        with open(path, "r") as f:
            data = json5.load(f)
        player = Player(name)
        player.load(data)
        print(TEXT["start_2"].format(player.name))
        return player

    def create_archive() -> Player:
        name = input(TEXT["start_3"])
        if name == "-1":
            return None
        return Player(name)

    print(TEXT["start_4"])
    while True:
        option = input(TEXT["start_5"])
        if option == "1":
            player = open_archive()
            if player is None:
                continue
            break
        elif option == "2":
            player = create_archive()
            if player is None:
                continue
            break
        elif option == "3":
            print(TEXT["game_close"])
            exit()
        else:
            print(TEXT["input_error"])
    main(player)


def other(player: Player) -> None:
    global TEXT, DATA, CROPS, ANIMALS
    option = input(TEXT["other_0"])
    if option == "1":
        while True:
            print(TEXT["other_1"])
            for i in DATA["language_list"]:
                print(i)
            language = input(TEXT["other_2"])
            if language in DATA["language_list"]:
                TEXT, DATA, CROPS, ANIMALS = init(root, language)
                break
            print(TEXT["input_error"])
    elif option == "2":
        if player.save_archive(root):
            print(TEXT["other_3"])
        else:
            print(TEXT["other_4"])
            other()
    elif option == "3":
        f = input(TEXT["other_5"])
        if f == "Yes" or f == "yes" or f == "y" or f == "Y":
            print(TEXT["game_close"])
            exit()
        else:
            print(TEXT["other_6"])
    elif option != "4":
        print(TEXT["input_error"])
        other(player)


def farm_op(c: list[int], player: Player) -> None:
    while True:
        option = input(TEXT["farm_op_0"])
        if option == "1":
            print(TEXT["farm_op_1"])
            player.bag.show("seed")
            select = input(TEXT["farm_op_2"])
            if select == "-1":
                continue
            try:
                select = int(select)
            except:
                print(TEXT["input_not_int"])
                continue
            for i in player.bag:
                if DATA["seed"][i]["id"] == select:
                    select = i
                    player.bag[i] -= 1
                    break
            else:
                print(TEXT["farm_op_3"])
                continue
            for i in c:
                v = player.farmland[i]
                if v.crop != "":
                    f = input(TEXT["farm_op_4"].format(i, TEXT[v.crop]))
                    if f != "Yes" and f != "yes" and f != "y" and f != "Y":
                        continue
                v.weed_appear = False
                v.bug_number -= random.randrange(v.bug_number)
                v.weed_appear_prob = max(0, v.weed_appear_prob - random.random())
                v.crop = select
                v.growth_time = 0
                v.ripe = False
        elif option == "2":
            print(TEXT["farm_op_5"].format(player.bag["organic_fertilizer"], player.bag["chemical_fertilizer"]))
            f = input(TEXT["farm_op_6"])
            if f == "1":
                f = "organic_fertilizer"
            elif f == "2":
                f = "chemical_fertilizer"
                t = False
            elif f == "3":
                continue
            else:
                print(TEXT["input_error"])
                continue
            if player.bag[f] < len(c):
                print(TEXT["farm_op_7"].format(TEXT[f]))
                continue
            player.bag[f] -= len(c)
            for i in c:
                v = player.farmland[i]
                v.soil_fertility += 1
                if not t:
                    v.organic = False
                if t:
                    v.bug_appear_prob += random() / 10
                else:
                    v.weed_appear_prob += random() / 10
        elif option == "3":
            print(TEXT["farm_op_8"])
            harvest = Bag()
            for i in c:
                v = player.farmland[i]
                if v.ripe:
                    harvest[v.crop] += 1
                v.crop = ""
                v.weed_appear = False
                v.growth_time = 0
                v.ripe = False
                v.bug_number -= random.randrange(v.bug_number)
                v.weed_appear_prob = max(0, v.weed_appear_prob - random.random())
                v.bug_appear_prob = max(0, v.bug_appear_prob - random.random())
            print(TEXT["farm_op_9"])
            harvest.show()
            player.bag.add(harvest)
        elif option == "4":
            print(TEXT["farm_op_10"].format(player.bag["herbicide"]))
            f = input(TEXT["farm_op_11"])
            if f == "1":
                if player.bag["herbicide"] < len(c):
                    print(TEXT["farm_op_12"])
                    continue
                player.bag["herbicide"] -= len(c)
                for i in c:
                    v = player.farmland[i]
                    v.organic = False
                    v.weed_appear = False
                    v.weed_appear_prob = max(0, v.weed_appear_prob - random.random())
            elif f == "2":
                for i in c:
                    v = player.farmland[i]
                    v.weed_appear = random.choice((False, True))
                    v.weed_appear_prob = max(0, v.weed_appear_prob - random.random() / 2)
            elif f == "3":
                continue
            else:
                print(TEXT["input_error"])
                continue
        elif option == "5":
            print(TEXT["farm_op_13"].format(player.bag["insecticide"]))
            f = input(TEXT["farm_op_14"])
            if f == "1":
                if player.bag["insecticide"] < len(c):
                    print(TEXT["farm_op_15"])
                    continue
                player.bag["insecticide"] -= len(c)
                for i in c:
                    v = player.farmland[i]
                    v.organic = False
                    v.bug_number -= random.randrange(v.bug_number)
                    v.bug_appear_prob = max(0, v.bug_appear_prob - random.random())
            elif f == "2":
                for i in c:
                    v = player.farmland[i]
                    v.bug_number -= random.randrange(v.bug_number) // 2
                    v.bug_appear_prob = max(0, v.bug_appear_prob - random.random() / 2)
            elif f == "3":
                continue
            else:
                print(TEXT["input_error"])
                continue
        elif option == "6":
            farm_info = Table(TEXT["farm_info"])
            for i in c:
                v = player.farmland[i]
                if v.crop == "":
                    farm_info.add([i, "Null", "0/0", v.soil_fertility, "0%", 0, "0%", False, False, True])
                else:
                    farm_info([i, TEXT[v.crop], f"{v.growth_time}/{CROPS[v.crop]["growth_time"]}", v.soil_fertility, f"{round(v.bug_appear_prob*100, 2)}%", v.bug_number, f"{round(v.weed_appear_prob*100, 2)}%", v.weed_appear, v.ripe, v.organic])
            farm_info.show()
        elif option == "7":
            break
        else:
            print(TEXT["input_error"])


def farmland(player: Player) -> None:
    while True:
        option = input(TEXT["farmland_0"])
        if option == "1":
            n = input(TEXT["farmland_1"])
            if n == "-1":
                continue
            elif n == "all":
                farm_op(list(range(len(player.farmland))), player)
            elif "~" in n:
                n.replace(" ", "")
                n = n.split("~", 1)
                try:
                    n[0] = int(n[0])
                    n[1] = int(n[1])
                except:
                    print(TEXT["input_not_int"])
                    continue
                if n[0] > n[1]:
                    n[0], n[1] = n[1], n[0]
                if 0 > n[0] or n[0] >= len(player.farmland):
                    print(TEXT["farmland_2"].format(n[0]))
                    continue
                if 0 > n[1] or n[1] >= len(player.farmland):
                    print(TEXT["farmland_2"].format(n[1]))
                    continue
                farm_op(list(range(n[0], n[1] + 1)), player)
            else:
                n = n.split()
                if len(n) == 1:
                    try:
                        n = int(n[0])
                    except:
                        print(TEXT["input_not_int"])
                        continue
                    if 0 > n or n >= len(player.farmland):
                        print(TEXT["farmland_2"].format(n))
                        continue
                    farm_op([n], player)
                    continue
                c = []
                for i in len(n):
                    try:
                        n[i] = int(n[i])
                    except:
                        print(TEXT["input_not_int"])
                        break
                    if 0 <= n[i] < len(player.farmland):
                        c.append(n[i])
                    else:
                        print(TEXT["farmland_2"].format(n[i]))
                        break
                else:
                    farm_op(c, player)
        elif option == "2":
            print(TEXT["farmland_3"], len(player.farmland))
            farm_info = Table(TEXT["farm_info"])
            for i, v in enumerate(player.farmland):
                if v.crop == "":
                    farm_info.add([i, "Null", "0/0", v.soil_fertility, "0%", 0, "0%", False, False, True])
                else:
                    farm_info([i, TEXT[v.crop], f"{v.growth_time}/{CROPS[v.crop]["growth_time"]}", v.soil_fertility, f"{round(v.bug_appear_prob*100, 2)}%", v.bug_number, f"{round(v.weed_appear_prob*100, 2)}%", v.weed_appear, v.ripe, v.organic])
            farm_info.show()
        elif option == "3":
            return
        else:
            print(TEXT["input_error"])


def next_day(player: Player) -> None:
    print(TEXT["next_day_0"])
    print("Zzz")
    player.day += 1
    print(TEXT["next_day_1"].format(player.day))
    for i in player.farmland:
        i.next_day()
    for i in player.corral:
        i.next_day()


def main(player: Player) -> None:
    print(TEXT["main_0"])
    while True:
        option = input(TEXT["main_1"])
        if option == "1":
            farmland(player)
        elif option == "2":
            pass
        elif option == "3":
            pass
        elif option == "4":
            next_day(player)
        elif option == "5":
            other(player)
        else:
            print(TEXT["input_error"])


if __name__ == "__main__":
    root = os.path.abspath(".")
    if root.endswith("\\source"):
        root = root[:-7]
    TEXT, DATA, CROPS, ANIMALS = init(root, "zh-tw")
    start()
