from typing import Optional

from data import Crop, Animal


class Farmland:
    def __init__(self) -> None:
        self.crop: Optional[Crop] = None
        self.growth_time = 0
        self.soil_fertility = 10
        self.bug_appear_prob = 0.1
        self.bug_number = 0
        self.weed_appear_prob = 0.1
        self.weed_appear = False
        self.ripe = False
        self.organic = True


class Corral:
    def __init__(self) -> None:
        self.animal: Optional[Animal] = None
        self.growth_time = 0
        self.neatness = 10
        self.manger: list[str] = []
        self.health = 100
        self.sick = False
        self.sick_prob = 0.1
        self.grow_up = False
        self.hunger = 0


class Bag:
    def __init__(self) -> None:
        self.items: dict[str, int] = {}
        self.seeds: dict[str, int] = {}
        self.crops: dict[str, int] = {}
        self.money = 100


class Player:
    def __init__(self) -> None:
        self.name = "username"
        self.day = 0
        self.bag = Bag()
        self.farmland: list[Farmland] = []
        self.corral: list[Corral] = []
        self.language = "en"
        self.farmland_size = 6
        self.corral_size = 6
        for _ in range(self.farmland_size):
            self.farmland.append(Farmland())
        for _ in range(self.corral_size):
            self.corral.append(Corral())
