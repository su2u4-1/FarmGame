from json import load
from os.path import dirname, abspath

from data import *
from player import *


def init(root_path: str) -> Data:
    with open(f"{root_path}/language/en.json", "r", encoding="utf-8") as f:
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
    return Data(text, items, seeds, crops, animals)


if __name__ == "__main__":
    root_path = abspath(dirname(__file__) + "/..").replace("\\", "/")
    DATA = init(root_path)
