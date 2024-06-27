import os.path
import json5

__all__ = ["init", "Bag", "Player", "TEXT", "DATA"]
TEXT: dict = {}
DATA: dict = {}


def init(root: str, language: str = "en") -> None:
    global TEXT, DATA
    path = os.path.join(root, "data", f"data.json5")
    with open(path, "r") as f:
        DATA = json5.load(f)
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

    def show(self) -> None:
        print("[名稱    ][數量]")
        for k, v in self.items():
            print(f"[{TEXT[k]:<6}][{v:<4}]")


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.money = 0
        self.bag = Bag()
        self.corral_n = 1
        self.farmland_n = 5
        self.day = 1
        self.stamina = 10
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
            f.write(json5.dumps(self.__dict__))
        return True
