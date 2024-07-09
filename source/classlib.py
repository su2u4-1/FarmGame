import os.path
from random import random
import json5

__all__ = ["init", "Bag", "Player", "TEXT", "DATA", "CROPS", "ANIMALS"]
N = dict[str : dict[str : int | list[str]]]
TEXT: dict[str:str] = {}
DATA: dict[str : N | list[str]] = {}
CROPS: N = {}
ANIMALS: N = {}


def init(root: str, language: str = "en") -> None:
    global TEXT, DATA, CROPS, ANIMALS
    path = os.path.join(root, "data", f"data.json5")
    with open(path, "r") as f:
        DATA = json5.load(f)
    CROPS = DATA["crops"]
    ANIMALS = DATA["animals"]
    path = os.path.join(root, "data", f"{language}.json5")
    if os.path.isfile(path):
        with open(path, "r") as f:
            TEXT = json5.load(f)
    else:
        path = os.path.join(root, "data", f"{DATA["language_list"][0]}.json5")
        with open(path, "r") as f:
            TEXT = json5.load(f)


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
                print("空無一物")
            else:
                print("[編號][名稱][數量]")
                for k, v in self.items():
                    if k in DATA["seed"]:
                        print(f"[{DATA["seed"][k]["id"]}][{TEXT[k]:<6}][{v:<4}]")
        else:
            if len(self) == 0:
                print("空無一物")
            else:
                print("[編號][名稱][數量]")
                for k, v in self.items():
                    if k in CROPS:
                        print(f"[{CROPS[k]["id"]}][{TEXT[k]}][{v}]")
                    if k in DATA["seed"]:
                        print(f"[{DATA["seed"][k]["id"]}][{TEXT[k]}][{v}]")
                    if k in ANIMALS:
                        print(f"[{ANIMALS[k]["id"]}][{TEXT[k]}][{v}]")


class farmland:
    def __init__(self):
        self.crop = ""
        self.growth_time = 0
        self.soil_fertility = 10
        self.bug_appear = 0.1
        self.bug_number = 0
        self.weed_appear_prob = 0.1
        self.weed_appear = False
        self.ripe = False
        self.organic = True

    def next_day(self) -> None:
        self.weed_appear_prob += random() / 10
        if random() <= self.weed_appear_prob:
            self.weed_appear = True
        if self.weed_appear:
            print(f"你的{TEXT[self.crop]}無法生長，因為出現雜草")
        elif self.growth_time != -1:
            self.growth_time += 1
        self.bug_appear += random() / 10
        if random() <= self.bug_appear:
            self.bug_number += 1
        if self.bug_number > CROPS[self.crop]["pest_resistance"]:
            print(f"你的{TEXT[self.crop]}死掉了，因為蟲子過多")
            self.growth_time = -1
        if CROPS[self.crop]["growth_time"] >= self.growth_time:
            self.ripe = True


class corral:
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
            print(f"你的{TEXT[self.animal]}死掉了，因為環境太過髒亂")


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.money = 0
        self.bag: Bag[str, int] = Bag()
        self.corral: list[corral] = [corral()]
        self.farmland: list[farmland] = [farmland()] * 5
        self.day = 1
        self.stamina = 10
        self.stamina_recovery_speed = 10
        self.stamina_max = 20

    def save_archive(self, root: str) -> bool:
        name = input("存檔名稱(輸入-1取消):")
        if name == "-1":
            return False
        path = os.path.join(root, "archive", name) + ".json5"
        if os.path.isfile(path):
            option = input("存檔已存在，是否要覆蓋(Yes/No):")
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
                    t[k].append(i.__dict__())
            elif k == "bag":
                t[k] = dict(v)
            else:
                t[k] = v

    def load(self, data: dict) -> None:
        for k, v in data.items():
            if k == "farmland":
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(farmland())
                    self.__dict__[k][-1].__dict__.update(i)
            elif k == "corral":
                self.__dict__[k] = []
                for i in v:
                    self.__dict__[k].append(corral())
                    self.__dict__[k][-1].__dict__.update(i)
            elif k == "bag":
                self.__dict__[k] = Bag(v)
            else:
                self.__dict__[k] = v
