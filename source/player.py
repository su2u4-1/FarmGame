from json import load
from typing import Optional, Sequence

from data import Crop, Animal


class Farmland:
    def __init__(
        self,
        crop: Optional[Crop] = None,
        growth_time: int = 0,
        soil_fertility: int = 10,
        bug_appear_prob: float = 0.1,
        bug_number: int = 0,
        weed_appear_prob: float = 0.1,
        weed_appear: bool = False,
        ripe: bool = False,
        organic: bool = True,
    ) -> None:
        self.crop = crop
        self.growth_time = growth_time
        self.soil_fertility = soil_fertility
        self.bug_appear_prob = bug_appear_prob
        self.bug_number = bug_number
        self.weed_appear_prob = weed_appear_prob
        self.weed_appear = weed_appear
        self.ripe = ripe
        self.organic = organic


class Corral:
    def __init__(
        self,
        animal: Optional[Animal] = None,
        growth_time: int = 0,
        neatness: int = 10,
        manger: Sequence[str] = (),
        health: int = 100,
        sick: bool = False,
        sick_prob: float = 0.1,
        grow_up: bool = False,
        hunger: int = 0,
    ) -> None:
        self.animal = animal
        self.growth_time = growth_time
        self.neatness = neatness
        self.manger = list(manger)
        self.health = health
        self.sick = sick
        self.sick_prob = sick_prob
        self.grow_up = grow_up
        self.hunger = hunger


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

    def load(self, file: str) -> int:
        try:
            with open(file, "r") as f:
                data = load(f)
        except FileNotFoundError | IOError as e:
            print(f"Error: {e}")
            return 1
        try:
            self.name = data["name"]
            self.day = data["day"]
            self.bag.items = data["bag"]["items"]
            self.bag.seeds = data["bag"]["seeds"]
            self.bag.crops = data["bag"]["crops"]
            self.bag.money = data["bag"]["money"]
            self.language = data["language"]
            self.farmland = []
            self.farmland_size = data["farmland_size"]
            for i in range(self.farmland_size):
                self.farmland.append(
                    Farmland(
                        crop=data["farmland"][i]["crop"],
                        growth_time=data["farmland"][i]["growth_time"],
                        soil_fertility=data["farmland"][i]["soil_fertility"],
                        bug_appear_prob=data["farmland"][i]["bug_appear_prob"],
                        bug_number=data["farmland"][i]["bug_number"],
                        weed_appear_prob=data["farmland"][i]["weed_appear_prob"],
                        weed_appear=data["farmland"][i]["weed_appear"],
                        ripe=data["farmland"][i]["ripe"],
                        organic=data["farmland"][i]["organic"],
                    )
                )
            self.corral = []
            self.corral_size = data["corral_size"]
            for i in range(self.corral_size):
                self.corral.append(
                    Corral(
                        animal=data["corral"][i]["animal"],
                        growth_time=data["corral"][i]["growth_time"],
                        neatness=data["corral"][i]["neatness"],
                        manger=data["corral"][i]["manger"],
                        health=data["corral"][i]["health"],
                        sick=data["corral"][i]["sick"],
                        sick_prob=data["corral"][i]["sick_prob"],
                        grow_up=data["corral"][i]["grow_up"],
                        hunger=data["corral"][i]["hunger"],
                    )
                )
        except KeyError as e:
            print(f"Error: {e}")
            return 2
        return 0

    def save(self) -> str:
        s = "{"
        s += f'"name": "{self.name}","day": {self.day},'
        s += '"bag": {"items": {'
        for k, v in self.bag.items.items():
            s += f'"{k}": {v},'
        s += '},"seeds": {'
        for k, v in self.bag.seeds.items():
            s += f'"{k}": {v},'
        s += '},"crops": {'
        for k, v in self.bag.crops.items():
            s += f'"{k}": {v},'
        s += "},"
        s += f'"money": {self.bag.money},'
        s += "},"
        s += f'"language": "{self.language}","farmland_size": {self.farmland_size},"farmland": ['
        for i in range(self.farmland_size):
            s += "{"
            s += f'"crop": "{self.farmland[i].crop}","growth_time": {self.farmland[i].growth_time},"soil_fertility": {self.farmland[i].soil_fertility},"bug_appear_prob": {self.farmland[i].bug_appear_prob},"bug_number": {self.farmland[i].bug_number},"weed_appear_prob": {self.farmland[i].weed_appear_prob},"weed_appear": {self.farmland[i].weed_appear},"ripe": {self.farmland[i].ripe},"organic": {self.farmland[i].organic}'
            s += "},"
        s += f'],corral_size": {self.corral_size},"corral": ['
        for i in range(self.corral_size):
            s += "{"
            s += f'"animal": "{self.corral[i].animal}","growth_time": {self.corral[i].growth_time},"neatness": {self.corral[i].neatness},"manger": {self.corral[i].manger},"health": {self.corral[i].health},"sick": {self.corral[i].sick},"sick_prob": {self.corral[i].sick_prob},"grow_up": {self.corral[i].grow_up},"hunger": {self.corral[i].hunger}'
            s += "},"
        s += "],}"
        return s
