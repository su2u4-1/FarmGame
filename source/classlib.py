import os.path
import random
from typing import Self, Any
import json5
from wcwidth import wcswidth


__all__ = ["init", "Bag", "Player", "Table", "My_dict"]
N = dict[str, dict[str, int | list[str]]]


class My_dict(dict[str, str]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> str:
        if key in self:
            return super().__getitem__(key)
        else:
            return super().__getitem__("text_not_found").format(key)

    def __setitem__(self, key: str, value: str) -> None:
        raise RuntimeError("No text changes allowed")


def init(root: str, language: str = "en") -> tuple[My_dict, dict[str, N | list[str]]]:
    global TEXT, DATA
    path = os.path.join(root, "data", f"data.json5")
    with open(path, "r") as f:
        DATA = json5.load(f)
    path = os.path.join(root, "data", f"{language}.json5")
    if os.path.isfile(path):
        with open(path, "r") as f:
            TEXT = My_dict(json5.load(f))
    else:
        path = os.path.join(root, "data", f"{DATA["language_list"][0]}.json5")
        with open(path, "r") as f:
            TEXT = My_dict(json5.load(f))
    return TEXT, DATA


class Bag(dict[str, int]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> int:
        if key in self:
            return super().__getitem__(key)
        else:
            super().__setitem__(key, 0)
            return 0

    def __setitem__(self, key: str, value: int) -> None:
        if value > 0:
            return super().__setitem__(key, value)
        elif value == 0:
            del self[key]
        else:
            raise RuntimeError(f"Item {key} quantity is negative.")

    def show(self, mode: str = "default") -> None:
        if mode == "seed" or mode == "crops" or mode == "animals":
            if sum(1 if k in DATA[mode] else 0 for k in self.keys()) == 0:
                print(TEXT["bag_0"])
            else:
                bag_item = Table(TEXT["bag_1"])
                for k, v in self.items():
                    if k in DATA[mode]:
                        bag_item.add([DATA[mode][k]["id"], TEXT[k], v])
                bag_item.show()
        else:
            if len(self) == 0:
                print(TEXT["bag_0"])
            else:
                bag_item = Table(TEXT["bag_1"])
                for k, v in self.items():
                    if k in DATA["crops"]:
                        bag_item.add([DATA["crops"][k]["id"], TEXT[k], v])
                    if k in DATA["seed"]:
                        bag_item.add([DATA["seed"][k]["id"], TEXT[k], v])
                    if k in DATA["animals"]:
                        bag_item.add([DATA["animals"][k]["id"], TEXT[k], v])
                bag_item.show()

    def add(self, other: Self | dict[str, int]) -> None:
        for k, v in other.items():
            self[k] += v

    def find(self, range: str, n: int) -> tuple[str, bool]:
        self.show(range)
        select = input("所選物品id(輸入-1取消):")
        if select == "-1":
            return "", False
        try:
            select = int(select)
        except:
            print(TEXT["input_not_int"])
            return "", False
        for i in self:
            if DATA[range][i]["id"] == select:
                if self[i] < n:
                    print("物品數量過少")
                    return "", False
                select = i
                self[i] -= n
                return select, True
        else:
            print("所選物品不存在")
            return "", False


class Farmland:
    def __init__(self):
        self.crop = ""
        self.growth_time = 0
        self.soil_fertility = 10
        self.bug_appear_prob = 0.1
        self.bug_number = 0
        self.weed_appear_prob = 0.1
        self.weed_appear = False
        self.ripe = False
        self.organic = True

    def next_day(self) -> None:
        if self.crop != "":
            self.weed_appear_prob += random.random() / 10
            if random.random() <= self.weed_appear_prob:
                self.weed_appear = True
            if self.weed_appear:
                print(TEXT["class_0"].format(TEXT[self.crop]))
            elif self.growth_time != -1:
                self.growth_time += 1
            self.bug_appear_prob += random.random() / 10
            if random.random() <= self.bug_appear_prob:
                self.bug_number += 1
            if self.bug_number > DATA["crops"][self.crop]["pest_resistance"]:
                print(TEXT["class_1"].format(TEXT[self.crop]))
                self.growth_time = -1
            if DATA["crops"][self.crop]["growth_time"] >= self.growth_time:
                self.ripe = True


class Corral:
    def __init__(self):
        self.animal = ""
        self.growth_time = 0
        self.neatness = 10
        self.manger = []
        self.health = 100
        self.sick = False
        self.sick_prob = 0.1
        self.grow_up = False
        self.hunger = 0

    def next_day(self) -> None:
        if self.animal != "":
            self.neatness -= random.random() / 10
            if self.neatness < 0:
                self.health -= random.random() * abs(self.neatness) * 10
            self.sick_prob += random.random() / 10
            if random.random() <= self.sick_prob:
                self.sick = True
            if self.sick:
                self.health -= random.random() * 10
            if self.health <= 0:
                print(TEXT["class_2"].format(TEXT[self.animal]))
                self.growth_time = -1
            if DATA["animals"][self.animal]["required_neatness"] >= self.neatness and not self.sick and self.growth_time != -1:
                self.growth_time += 1
            if DATA["animals"][self.animal]["growth_time"] >= self.growth_time:
                self.grow_up = True
            for _ in range(random.randrange(5) + 1):
                if len(self.manger) > 0:
                    self.eat()
            self.hunger -= 1
            if self.sick:
                self.hunger -= 1
            if self.hunger <= 0:
                print(TEXT["class_5"].format(TEXT[self.animal]))
                self.growth_time = -1

    def eat(self):
        for i in self.manger:
            if i in DATA["animals"][self.animal]["food"]:
                self.manger.remove(i)
                self.hunger += 1
                return


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.money = 0
        self.bag = Bag()
        self.farmland = [Farmland()] * 5
        self.corral = [Corral()]
        self.day = 1

    def save_archive(self, root: str) -> bool:
        name = input(TEXT["class_3"])
        if name == "-1":
            return False
        path = os.path.join(root, "archive", name) + ".json5"
        if os.path.isfile(path):
            option = input(TEXT["class_4"])
            if option != "Yes" and option != "yes" and option != "y" and option != "Y":
                return False
        with open(path, "+w") as f:
            f.write(json5.dumps(self.serialize()))
        return True

    def serialize(self) -> dict[str, Any]:
        t = {}
        for k, v in self.__dict__.items():
            if k == "farmland" or k == "corral":
                t[k] = []
                for i in v:
                    t[k].append(i.__dict__)
            elif k == "bag":
                t[k] = dict(v)
            else:
                t[k] = v
        return t

    def load(self, data: dict[str, Any]) -> None:
        for k, v in data.items():
            if k == "farmland":
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(Farmland())
                    self.__dict__[k][-1].__dict__.update(i)
            elif k == "corral":
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(Corral())
                    self.__dict__[k][-1].__dict__.update(i)
            elif k == "bag":
                self.__dict__[k] = Bag(v)
            else:
                self.__dict__[k] = v


class Table:
    def __init__(self, title: list[object] | str) -> None:
        if type(title) == str:
            title = title.split("|")
        self.data = [title]
        self.length = [wcswidth(str(i)) for i in title]
        self.n = len(title)

    def add(self, d: list[object]) -> None:
        if len(d) != self.n:
            raise ValueError(f"The length is different from the information above.\ntitle: {self.data[0]}\nnew: {d}")
        self.data.append(d)
        for i in range(self.n):
            self.length[i] = max(self.length[i], wcswidth(str(d[i])))

    def show(self) -> None:
        for j in self.data:
            for i in range(self.n):
                print(f"[{j[i]}", end="")
                print(" " * (self.length[i] - wcswidth(str(j[i]))), end="]")
            print()
