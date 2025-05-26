from random import choices
from random import randint as ri
from typing import Literal, Optional, SupportsIndex

from data import Data
from player import DefaultDict, Player


def limit_range(
    value: float,
    operator: Literal["+", "-", "*", "/"],
    ratio: float,
    min_value: float = 0.01,
    max_value: float = 1,
    n_digits: Optional[SupportsIndex] = 2,
) -> float | int:
    """
    Limit the value to a specified range and round it to a specified number of decimal places.

    Args:
        value (float): The value to limit.
        operator (str): The operator to use for limiting the value. Can be "+", "-", "*", or "/".
        ratio (float): The ratio to apply to the value.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.
        n_digits (int): The number of decimal places to round to.

    Returns:
        float: The limited and rounded value.
    """
    match operator:
        case "+":
            return round(max(min(value + ratio, max_value), min_value), n_digits)
        case "-":
            return round(max(min(value - ratio, max_value), min_value), n_digits)
        case "*":
            return round(max(min(value * ratio, max_value), min_value), n_digits)
        case "/":
            if ratio == 0:
                return round(max(min(value, max_value), min_value), n_digits)
            else:
                return round(max(min(value / ratio, max_value), min_value), n_digits)


def plant(player: Player, choices_farmland_id: tuple[int, ...], choice_seed_id: str) -> None:
    player.bag.seeds[choice_seed_id] -= len(choices_farmland_id)
    for i in choices_farmland_id:
        player.farmland[i].crop = choice_seed_id.removesuffix("_seed")


def fertilize(player: Player, choices_farmland_id: tuple[int, ...], organic: bool) -> None:
    player.bag.items["organic_fertilizer" if organic else "chemical_fertilizer"] -= len(choices_farmland_id)
    for i in choices_farmland_id:
        player.farmland[i].soil_fertility += ri(1, ri(3, 5))
        if organic:
            player.farmland[i].bug_appear_prob += 0.05
        else:
            player.farmland[i].organic = False


def harvest_remove(player: Player, choices_farmland_id: tuple[int, ...]) -> dict[str, int]:
    crops: DefaultDict[str, int] = DefaultDict(lambda _: 0, lambda _: 0)
    for i in choices_farmland_id:
        i = player.farmland[i]
        if i.crop != "":
            i.bug_appear_prob = limit_range(i.bug_appear_prob, "/", ri(150, 250) / 100)
            i.bug_number = 0
            i.weed_appear_prob = limit_range(i.weed_appear_prob, "/", ri(150, 250) / 100)
            i.weed_appear = False
            i.growth_time = 0
            if i.ripe:
                crop_name = i.crop.removesuffix("_seed")
                crops[crop_name] = crops[crop_name] + 1
            else:
                i.soil_fertility = int(limit_range(i.soil_fertility, "*", ri(100, 150) / 100, 1, 50, None))
            i.ripe = False
            i.crop = ""
    return crops


def weed(player: Player, choices_farmland_id: tuple[int, ...], herbicide: bool) -> None:
    if herbicide:
        player.bag.items["herbicide"] -= len(choices_farmland_id)
        for i in choices_farmland_id:
            i = player.farmland[i]
            i.weed_appear_prob = limit_range(i.weed_appear_prob, "/", ri(200, 300) / 100)
            i.weed_appear = False
            i.organic = False
    else:
        for i in choices_farmland_id:
            i = player.farmland[i]
            i.weed_appear_prob = limit_range(i.weed_appear_prob, "/", ri(150, 250) / 100)
            i.weed_appear = False


def disinfestation(player: Player, choices_farmland_id: tuple[int, ...], insecticide: bool) -> None:
    if insecticide:
        player.bag.items["insecticide"] -= len(choices_farmland_id)
        for i in choices_farmland_id:
            i = player.farmland[i]
            i.bug_appear_prob = limit_range(i.bug_appear_prob, "/", ri(200, 300) / 100)
            i.bug_number = ri(0, i.bug_number // 10)
            i.organic = False
    else:
        for i in choices_farmland_id:
            i = player.farmland[i]
            i.bug_appear_prob = limit_range(i.bug_appear_prob, "/", ri(150, 250) / 100)
            i.bug_number = ri(0, i.bug_number // 5)


def next_day(player: Player, data: Data) -> None:
    for i in player.farmland:
        if i.crop != "":
            if i.ripe:
                i.bug_appear_prob = limit_range(i.bug_appear_prob, "+", ri(5, 50) / 100)
            else:
                i.bug_appear_prob = limit_range(i.bug_appear_prob, "+", ri(1, 30) / 100)
            if i.bug_appear_prob * 100 > ri(0, 100):
                i.bug_number += 1
            i.weed_appear_prob = limit_range(i.weed_appear_prob, "+", ri(1, 30) / 100)
            if i.weed_appear_prob * 100 > ri(0, 100):
                i.weed_appear = True
            if data.crops[i.crop].pest_resistance <= i.bug_number:
                print(data.text["class_1"].format(data.text[i.crop]))
                i.crop = ""
                i.growth_time = 0
                i.ripe = False
                i.organic = True
            if i.weed_appear:
                i.soil_fertility -= choices((1, 2, 3), (12, 3, 1))[0]
            if i.soil_fertility >= data.crops[i.crop].soil_needed:
                i.soil_fertility -= data.crops[i.crop].soil_needed
                i.growth_time += 1
            else:
                print(data.text["class_0"].format(data.text[i.crop]))
            if i.growth_time >= data.crops[i.crop].growth_time:
                i.ripe = True
        elif i.soil_fertility > 0:
            i.soil_fertility -= 1
    for i in player.corral:
        pass
