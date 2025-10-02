from json import load
from typing import Any, Callable, Sequence, TypeVar
from time import localtime


def get_time() -> str:
    return f"{localtime().tm_year}-{localtime().tm_mon:02}-{localtime().tm_mday:02} {localtime().tm_hour:02}:{localtime().tm_min:02}:{localtime().tm_sec:02}"


class Farmland:
    def __init__(
        self,
        crop: str = "",
        growth_time: int = 0,
        soil_fertility: int = 10,
        bug_appear_prob: float = 0.05,
        bug_number: int = 0,
        weed_appear_prob: float = 0.05,
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
        animal: str = "",
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


K = TypeVar("K")
V = TypeVar("V")


class DefaultDict(dict[K, V]):
    def __init__(self, default_factory: Callable[[K], V], delete_value: Callable[[K], V], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, *kwargs)
        self.default_factory = default_factory
        self.delete_value = delete_value

    def __missing__(self, key: K) -> V:
        return self.default_factory(key)

    def __getitem__(self, key: K) -> V:
        if key in self:
            return super().__getitem__(key)
        return self.__missing__(key)

    def __setitem__(self, key: K, value: V) -> None:
        if value == self.delete_value(key):
            del self[key]
        else:
            super().__setitem__(key, value)


class Bag:
    def __init__(self) -> None:
        self.items: DefaultDict[str, int] = DefaultDict(lambda _: 0, lambda _: 0)
        self.seeds: DefaultDict[str, int] = DefaultDict(lambda _: 0, lambda _: 0)
        self.crops: DefaultDict[str, int] = DefaultDict(lambda _: 0, lambda _: 0)
        self.animals: DefaultDict[str, int] = DefaultDict(lambda _: 0, lambda _: 0)
        self.money = 100


class Player:
    def __init__(self) -> None:
        self.name = "username"
        self.day = 1
        self.bag = Bag()
        self.farmland: list[Farmland] = []
        self.corral: list[Corral] = []
        self.language = "zh-tw"
        self.farmland_size = 6
        self.corral_size = 6
        for _ in range(self.farmland_size):
            self.farmland.append(Farmland())
        for _ in range(self.corral_size):
            self.corral.append(Corral())
        self.energy = 100

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
            self.bag.items = DefaultDict(lambda _: 0, lambda _: 0, data["bag"]["items"])
            self.bag.seeds = DefaultDict(lambda _: 0, lambda _: 0, data["bag"]["seeds"])
            self.bag.crops = DefaultDict(lambda _: 0, lambda _: 0, data["bag"]["crops"])
            self.bag.animals = DefaultDict(lambda _: 0, lambda _: 0, data["bag"]["animals"])
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
            self.energy = data["energy"]
        except KeyError as e:
            print(f"Error: {e}")
            return 2
        return 0

    def save(self) -> str:
        t: list[str] = []
        s = "{" + f'"name": "{self.name}","day": {self.day},' + '"bag": {"items": {'
        for k, v in self.bag.items.items():
            t.append(f'"{k}": {v}')
        s += ",".join(t)
        t = []
        s += '},"seeds": {'
        for k, v in self.bag.seeds.items():
            t.append(f'"{k}": {v}')
        s += ",".join(t)
        t = []
        s += '},"crops": {'
        for k, v in self.bag.crops.items():
            t.append(f'"{k}": {v}')
        s += ",".join(t)
        t = []
        s += '},"animals": {'
        for k, v in self.bag.animals.items():
            t.append(f'"{k}": {v}')
        s += ",".join(t)
        t = []
        s += "}," + f'"money": {self.bag.money}' + "}," + f'"language": "{self.language}","farmland_size": {self.farmland_size},"farmland": ['
        for i in range(self.farmland_size):
            t.append(
                "{"
                + f'"crop": "{self.farmland[i].crop}","growth_time": {self.farmland[i].growth_time},"soil_fertility": {self.farmland[i].soil_fertility},"bug_appear_prob": {self.farmland[i].bug_appear_prob},"bug_number": {self.farmland[i].bug_number},"weed_appear_prob": {self.farmland[i].weed_appear_prob},"weed_appear": {"true" if self.farmland[i].weed_appear else "false"},"ripe": {"true" if self.farmland[i].ripe else "false"},"organic": {"true" if self.farmland[i].organic else " false"}'
                + "}"
            )
        s += ",".join(t)
        t = []
        s += f'],"corral_size": {self.corral_size},"corral": ['
        for i in range(self.corral_size):
            t.append(
                "{"
                + f'"animal": "{self.corral[i].animal}","growth_time": {self.corral[i].growth_time},"neatness": {self.corral[i].neatness},"manger": {self.corral[i].manger},"health": {self.corral[i].health},"sick": {"true" if self.corral[i].sick else "false"},"sick_prob": {self.corral[i].sick_prob},"grow_up": {"true" if self.corral[i].grow_up else "false"},"hunger": {self.corral[i].hunger}'
                + "}"
            )
        s += ",".join(t)
        s += "]," + f'"energy": {self.energy}'
        s += f', "time": "{get_time()}"' + "}"
        return s
