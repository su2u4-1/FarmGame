from data import Data
from player import Player
from ui import get_choice_in_options, get_range_input, DisplayInfo


def manage_corral(player: Player, data: Data, choices: tuple[int, ...]) -> None:
    while True:
        match get_choice_in_options(data.text["corral_op_0"], lambda x: 0 <= x < 7, data.text["input_error"], data.text["input_not_int"]):
            case 0:
                pass
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
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
                        )
                    )
                print(data.text["corral_3"].format(player.corral_size))
                info.display()
            case 2:
                return
