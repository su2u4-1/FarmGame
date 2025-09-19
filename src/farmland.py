from data import Data
from other import plant, fertilize, harvest_remove, weed, disinfestation
from player import Player
from ui import get_int_input, get_choice_in_options, get_bool_input, get_range_input, DisplayInfo


def manage_farmland(player: Player, data: Data, choices: tuple[int, ...]) -> None:
    while True:
        match get_choice_in_options(data.text["farm_op_0"], lambda x: 0 <= x < 7, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                m: dict[int, str] = {}
                info = DisplayInfo(data.text["farm_op_12"], data.text["no_item"])
                for i, (k, v) in enumerate(player.bag.seeds.items()):
                    info.add((i + 1, data.text[k], v))
                    m[i] = k
                print(data.text["farm_op_1"])
                info.display()
                choice_seed = get_int_input(data.text["farm_op_2"], lambda x: 0 <= x < len(m), data.text["farm_op_3"], data.text["input_not_int"])
                if choice_seed == -1:
                    continue
                if player.bag.seeds[m[choice_seed]] < len(choices):
                    print(data.text["farm_op_7"].format(data.text[m[choice_seed]]))
                    continue
                plant(player, choices, m[choice_seed])
                print(data.text["farm_op_14"])
            case 1:
                print(data.text["farm_op_5"].format(data.text["organic_fertilizer"], player.bag.items["organic_fertilizer"]))
                print(data.text["farm_op_5"].format(data.text["chemical_fertilizer"], player.bag.items["chemical_fertilizer"]))
                choice_fertilizer = get_choice_in_options(data.text["farm_op_6"], lambda x: 0 <= x < 3, data.text["farm_op_3"], data.text["input_not_int"])
                if choice_fertilizer == 2:
                    continue
                if choice_fertilizer == 0:
                    choice_fertilizer = "organic_fertilizer"
                else:
                    choice_fertilizer = "chemical_fertilizer"
                if player.bag.items[choice_fertilizer] < len(choices):
                    print(data.text["farm_op_7"].format(data.text[choice_fertilizer]))
                    continue
                fertilize(player, choices, choice_fertilizer == "organic_fertilizer")
                print(data.text["farm_op_18"])
            case 2:
                if not get_bool_input(data.text["farm_op_8"], False):
                    continue
                crops = harvest_remove(player, choices)
                print(data.text["farm_op_9"])
                info = DisplayInfo(data.text["farm_op_13"], data.text["no_item"])
                for k, v in crops.items():
                    info.add((data.text[k], v))
                    player.bag.crops[k] += v
                info.display()
            case 3:
                print(data.text["farm_op_5"].format(data.text["herbicide"], player.bag.items["herbicide"]))
                choice_herbicide = get_choice_in_options(data.text["farm_op_11"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"])
                if choice_herbicide == 2:
                    continue
                if choice_herbicide == 0 and player.bag.items["herbicide"] < len(choices):
                    print(data.text["farm_op_7"].format(data.text["herbicide"]))
                    continue
                if choice_herbicide == 1 and player.energy < len(choices):
                    print(data.text["farm_op_17"])
                    continue
                weed(player, choices, choice_herbicide == 0)
                print(data.text["farm_op_19"])
                if choice_herbicide == 1:
                    print(data.text["farm_op_16"].format(player.energy))
            case 4:
                print(data.text["farm_op_5"].format(data.text["insecticide"], player.bag.items["insecticide"]))
                choice_insecticide = get_choice_in_options(data.text["farm_op_10"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"])
                if choice_insecticide == 2:
                    continue
                if choice_insecticide == 0 and player.bag.items["insecticide"] < len(choices):
                    print(data.text["farm_op_7"].format(data.text["insecticide"]))
                    continue
                if choice_insecticide == 1 and player.energy < len(choices):
                    print(data.text["farm_op_17"])
                    continue
                disinfestation(player, choices, choice_insecticide == 0)
                print(data.text["farm_op_20"])
                if choice_insecticide == 1:
                    print(data.text["farm_op_16"].format(player.energy))
            case 5:
                info = DisplayInfo(data.text["farmland_info"], data.text["no_item"])
                for i in choices:
                    j = player.farmland[i]
                    info.add(
                        (
                            i + 1,
                            data.text[j.crop] if j.crop != "" else data.text["empty"],
                            j.growth_time,
                            j.soil_fertility,
                            j.bug_appear_prob,
                            j.bug_number,
                            j.weed_appear_prob,
                            "O" if j.weed_appear else "X",
                            "O" if j.ripe else "X",
                            "O" if j.organic else "X",
                        )
                    )
                print(data.text["farmland_3"].format(len(choices)))
                info.display()
            case 6:
                return


def farmland(player: Player, data: Data) -> None:
    while True:
        match get_choice_in_options(data.text["farmland_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                choices = get_range_input(
                    data.text["farmland_1"],
                    lambda x: 0 <= x < player.farmland_size,
                    data.text["farmland_2"],
                    data.text["input_not_int"],
                    data.text["format_error"],
                )
                if choices == (-1,):
                    continue
                elif choices == (-2,):
                    choices = tuple(range(player.farmland_size))
                manage_farmland(player, data, choices)
            case 1:
                info = DisplayInfo(data.text["farmland_info"], data.text["no_item"])
                for i in range(player.farmland_size):
                    j = player.farmland[i]
                    info.add(
                        (
                            i + 1,
                            data.text[j.crop] if j.crop != "" else data.text["empty"],
                            j.growth_time,
                            j.soil_fertility,
                            j.bug_appear_prob,
                            j.bug_number,
                            j.weed_appear_prob,
                            "O" if j.weed_appear else "X",
                            "O" if j.ripe else "X",
                            "O" if j.organic else "X",
                        )
                    )
                print(data.text["farmland_3"].format(player.farmland_size))
                info.display()
            case 2:
                return
