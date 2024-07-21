import os.path
from random import random
from typing import Self
import json5
from wcwidth import wcswidth


__all__ = ["init", "Bag", "Player", "Table", "My_dict"]
N = dict[str : dict[str : int | list[str]]]


class My_dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> str:
        if key in self:
            return super().__getitem__(key)
        else:
            return super().__getitem__("text_not_found").format(key)

    def __setitem__(self, key: str, value: str) -> None:
        raise RuntimeError("No text changes allowed")


def init(root: str, language: str = "en") -> tuple[My_dict[str:str], dict[str : N | list[str]], N, N]:
    global TEXT, DATA, CROPS, ANIMALS
    path = os.path.join(root, "data", f"data.json5")
    with open(path, "r") as f:
        DATA = json5.load(f)
    CROPS = DATA["crops"]
    ANIMALS = DATA["animals"]
    path = os.path.join(root, "data", f"{language}.json5")
    if os.path.isfile(path):
        with open(path, "r") as f:
            TEXT = My_dict(json5.load(f))
    else:
        path = os.path.join(root, "data", f"{DATA["language_list"][0]}.json5")
        with open(path, "r") as f:
            TEXT = My_dict(json5.load(f))
    return TEXT, DATA, CROPS, ANIMALS


class Bag(dict):
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
        if mode == "seed":
            if sum(1 if k in DATA["seed"] else 0 for k in self.keys()) == 0:
                print(TEXT["bag_0"])
            else:
                bag_item = Table(TEXT["bag_1"])
                for k, v in self.items():
                    if k in DATA["seed"]:
                        bag_item.add([DATA["seed"][k]["id"], TEXT[k], v])
                bag_item.show()
        else:
            if len(self) == 0:
                print(TEXT["bag_0"])
            else:
                bag_item = Table(TEXT["bag_1"])
                for k, v in self.items():
                    if k in CROPS:
                        bag_item.add([CROPS[k]["id"], TEXT[k], v])
                    if k in DATA["seed"]:
                        bag_item.add([DATA["seed"][k]["id"], TEXT[k], v])
                    if k in ANIMALS:
                        bag_item.add([ANIMALS[k]["id"], TEXT[k], v])
                bag_item.show()

    def add(self, other: Self | dict) -> None:
        for k, v in other.items():
            self[k] += v


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
            self.weed_appear_prob += random() / 10
            if random() <= self.weed_appear_prob:
                self.weed_appear = True
            if self.weed_appear:
                print(TEXT["class_0"].format(TEXT[self.crop]))
            elif self.growth_time != -1:
                self.growth_time += 1
            self.bug_appear_prob += random() / 10
            if random() <= self.bug_appear_prob:
                self.bug_number += 1
            if self.bug_number > CROPS[self.crop]["pest_resistance"]:
                print(TEXT["class_1"].format(TEXT[self.crop]))
                self.growth_time = -1
            if CROPS[self.crop]["growth_time"] >= self.growth_time:
                self.ripe = True


class Corral:
    def __init__(self):
        self.animal = ""
        self.growth_time = 0
        self.neatness = 10
        self.manger = []

    def next_day(self) -> None:
        self.neatness -= random()
        if ANIMALS[self.animal]["required_neatness"] >= self.neatness:
            self.growth_time += 1
        if self.neatness < 0:
            print(TEXT["class_2"].format(TEXT[self.animal]))


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.money = 0
        self.bag: Bag[str, int] = Bag()
        self.farmland: list[Farmland] = [Farmland()] * 5
        self.corral: list[Corral] = [Corral()]
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

    def serialize(self) -> dict:
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

    def load(self, data: dict) -> None:
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
    def __init__(self, title: list | str) -> None:
        if type(title) == str:
            title = title.split("|")
        self.data = [title]
        self.length = [wcswidth(str(i)) for i in title]
        self.n = len(title)

    def add(self, d: list) -> None:
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
