from typing import Literal

from data import Data
from other import limit_range
from player import Player
from ui import get_int_input, DisplayInfo


def buy(player: Player, data: Data, kind: Literal["seeds", "items", "crops", "animals"]) -> None:
    match kind:
        case "seeds":
            bag = player.bag.seeds
            now_data = data.seeds
        case "items":
            bag = player.bag.items
            now_data = data.items
        case "crops":
            bag = player.bag.crops
            now_data = data.crops
        case "animals":
            bag = player.bag.animals
            now_data = data.animals
    while True:
        info = DisplayInfo(data.text["shop_0"], data.text["no_item"])
        d: dict[int, str] = {}
        for i, (k, v) in enumerate(now_data.items()):
            info.add((i + 1, data.text[k], int(limit_range(v.sell_price, "*", 1.2, 1, float("inf"), 0))))
            d[i] = k
        print(data.text["shop_1"].format(player.bag.money))
        print(data.text["shop_7"])
        info.display()
        result = get_int_input(data.text["shop_8"], lambda x: 0 <= x < len(now_data), data.text["input_error"], data.text["input_not_int"])
        if result == -1:
            return
        choice = d[result]
        buy_price = int(limit_range(now_data[choice].sell_price, "*", 1.2, 1, float("inf"), 0))
        buy_number = 1 + get_int_input(
            data.text["shop_9"],
            lambda x: 0 <= x < player.bag.money // buy_price,
            data.text["shop_10"],
            data.text["input_not_int"],
        )
        if buy_number <= 0:
            return
        bag[choice] = bag[choice] + buy_number
        player.bag.money -= buy_number * buy_price
        print(data.text["shop_11"].format(buy_number, data.text[choice], buy_price * buy_number))


def sell(player: Player, data: Data, kind: Literal["seeds", "items", "crops", "animals"]) -> None:
    match kind:
        case "seeds":
            bag = player.bag.seeds
            now_data = data.seeds
        case "items":
            bag = player.bag.items
            now_data = data.items
        case "crops":
            bag = player.bag.crops
            now_data = data.crops
        case "animals":
            bag = player.bag.animals
            now_data = data.animals
    while True:
        info = DisplayInfo(data.text["shop_0"], data.text["no_item"])
        d: dict[int, str] = {}
        for i, (k, v) in enumerate(bag.items()):
            info.add((i + 1, data.text[k], now_data[k].sell_price, v))
            d[i] = k
        print(data.text["shop_1"].format(player.bag.money))
        print(data.text["shop_2"])
        info.display()
        result = get_int_input(data.text["shop_3"], lambda x: 0 <= x < len(bag), data.text["input_error"], data.text["input_not_int"])
        if result == -1:
            return
        choice = d[result]
        sell_number = 1 + get_int_input(data.text["shop_4"], lambda x: 0 <= x < bag[choice], data.text["shop_5"], data.text["input_not_int"], lambda x: x == "all", -2)
        if sell_number == -2 + 1:
            sell_number = bag[choice]
        elif sell_number <= 0:
            return
        bag[choice] -= sell_number
        player.bag.money += sell_number * now_data[choice].sell_price
        print(data.text["shop_6"].format(sell_number, data.text[choice], now_data[choice].sell_price * sell_number))
