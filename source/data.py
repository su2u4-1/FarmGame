from collections.abc import Mapping


class Item:
    def __init__(self, ID: str) -> None:
        self.ID = ID


class Seed:
    def __init__(self, ID: str) -> None:
        self.ID = ID


class Crop:
    def __init__(self, growth_time: int, seed_price: int, sell_price: int, soil_needed: int, pest_resistance: int) -> None:
        self.growth_time = growth_time
        self.seed_price = seed_price
        self.sell_price = sell_price
        self.soil_needed = soil_needed
        self.pest_resistance = pest_resistance


class Animal:
    def __init__(self, baby_price: int, growth_time: int, adult_sell_price: int, food: tuple[str], food_needed_per_day: int, required_neatness: int) -> None:
        self.baby_price = baby_price
        self.growth_time = growth_time
        self.adult_sell_price = adult_sell_price
        self.food = food
        self.food_needed_per_day = food_needed_per_day
        self.required_neatness = required_neatness


class Text(dict[str, str]):
    def __init__(self, map: Mapping[str, str] = {}, **kwargs: str) -> None:
        super().__init__(map, **kwargs)

    def __getitem__(self, key: str) -> str:
        if key in self:
            return super().__getitem__(key)
        else:
            return super().__getitem__("text_not_found").format(key)

    def __setitem__(self, key: str, value: str) -> None:
        raise KeyError("You can't set a value in this dictionary.")


class Data:
    def __init__(self, text: Text, items: dict[str, Item], seeds: dict[str, Seed], crops: dict[str, Crop], animals: dict[str, Animal]) -> None:
        self.text = text
        self.items = items
        self.seeds = seeds
        self.crops = crops
        self.animals = animals
