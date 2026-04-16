from data import Data
from player import Player
from ui import get_bool_input, get_choice_in_options, get_int_input, get_range_input, DisplayInfo
from other import put_in_animal, butcher, put_in_crop


def manage_corral(player: Player, data: Data, choices: tuple[int, ...]) -> None:
    while True:
        match get_choice_in_options(data.text["corral_op_0"], lambda x: 0 <= x < 8, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                m: dict[int, str] = {}
                info = DisplayInfo(data.text["corral_op_2"], data.text["no_item"])
                for i, (k, v) in enumerate(player.bag.animals.items()):
                    info.add((i + 1, data.text[k], v))
                    m[i] = k
                print(data.text["corral_op_1"])
                info.display()
                choice_animal = get_int_input(data.text["corral_op_3"], lambda x: 0 <= x < len(m), data.text["corral_op_4"], data.text["input_not_int"])
                if choice_animal == -1:
                    continue
                if player.bag.animals[m[choice_animal]] < len(choices):
                    print(data.text["corral_op_5"].format(data.text[m[choice_animal]]))
                    continue
                put_in_animal(player, choices, m[choice_animal])
                print(data.text["corral_op_6"])
            case 1:
                info = DisplayInfo(data.text["corral_op_10"], data.text["no_item"])
                for i in choices:
                    for k, v in player.corral[i].manger.items():
                        if v > 0:
                            info.add((i + 1, data.text[k], v))
                print(data.text["corral_op_11"])
                info.display()
                m: dict[int, str] = {}
                info = DisplayInfo(data.text["corral_op_10"], data.text["no_item"])
                for i, (k, v) in enumerate(player.bag.crops.items()):
                    info.add((i + 1, data.text[k], v))
                    m[i] = k
                print(data.text["corral_op_12"])
                info.display()
                choice_crop = get_int_input(data.text["corral_op_3"], lambda x: 0 <= x < len(player.bag.crops), data.text["corral_op_4"], data.text["input_not_int"])
                if choice_crop == -1:
                    continue
                if player.bag.crops[m[choice_crop]] < len(choices):
                    print(data.text["corral_op_5"].format(data.text[m[choice_crop]]))
                    continue
                put_in_crop(player, choices, m[choice_crop])
                print(data.text["corral_op_6"])
            case 2:
                if not get_bool_input(data.text["corral_op_7"], False, data.text["input_not_bool"]):
                    continue
                animals = butcher(player, choices)
                info = DisplayInfo(data.text["corral_op_8"], data.text["no_item"])
                for k, v in animals.items():
                    info.add((data.text[k], v))
                    player.bag.animals[k] += v
                print(data.text["corral_op_9"])
                info.display()
            case 3:
                pass
            case 4:
                pass
            case 5:
                info = DisplayInfo(data.text["corral_info"], data.text["no_item"])
                for i in choices:
                    j = player.corral[i]
                    info.add(
                        (
                            i + 1,
                            data.text[j.animal] if j.animal != "" else data.text["empty"],
                            j.growth_time,
                            j.hunger,
                            j.neatness,
                            j.health,
                            j.sick_prob,
                            "O" if j.sick else "X",
                            "O" if j.grow_up else "X",
                            ", ".join(data.text[k] if v == 1 else data.text[k] + f"x{v}" for k, v in j.manger.items() if v > 0),
                        )
                    )
                print(data.text["corral_3"].format(player.corral_size))
                info.display()
            case 6 | -1:
                return


def corral(player: Player, data: Data) -> None:
    while True:
        match get_choice_in_options(data.text["corral_0"], lambda x: 0 <= x < 3, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                choices = get_range_input(
                    data.text["corral_1"],
                    lambda x: 0 <= x < player.corral_size,
                    data.text["corral_2"],
                    data.text["input_not_int"],
                    data.text["format_error"],
                )
                if choices == (-1,):
                    continue
                elif choices == (-2,):
                    choices = tuple(range(player.corral_size))
                manage_corral(player, data, choices)
            case 1:
                info = DisplayInfo(data.text["corral_info"], data.text["no_item"])
                for i in range(player.corral_size):
                    j = player.corral[i]
                    info.add(
                        (
                            i + 1,
                            data.text[j.animal] if j.animal != "" else data.text["empty"],
                            j.growth_time,
                            j.hunger,
                            j.neatness,
                            j.health,
                            j.sick_prob,
                            "O" if j.sick else "X",
                            "O" if j.grow_up else "X",
                            ", ".join(data.text[k] if v == 1 else data.text[k] + f"x{v}" for k, v in j.manger.items() if v > 0),
                        )
                    )
                print(data.text["corral_3"].format(player.corral_size))
                info.display()
            case 2 | -1:
                return
