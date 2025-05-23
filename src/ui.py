from typing import Callable, Optional, Sequence, Union

from wcwidth import wcswidth


class Display_info:
    def __init__(self, title: Union[Sequence[object], str], empty_msg: str) -> None:
        """
        Initializes the Display_info class with a title.

        Args:
            title (list[object] | str): The title to display.
            empty_msg (str): The message to display when there are no items.
        """
        if isinstance(title, str):
            title = tuple(i.strip() for i in title.split("|"))
        else:
            title = tuple(str(t).strip() for t in title)
        self.show = [title]
        self.size = len(title)
        self.length: list[int] = [wcswidth(t) for t in title]
        self.empty_msg = empty_msg

    def add(self, item: Sequence[object]) -> None:
        """
        Adds an item to the display.
        Args:
            item (Sequence[object]): The item to add.
        Raises:
            ValueError: If the length of the item exceeds the title length.
        """
        if isinstance(item, str):
            item = tuple(i.strip() for i in item.split("|"))
        else:
            item = tuple(str(i).strip() for i in item)
        if len(item) > self.size:
            raise ValueError("Item length exceeds title length.")
        elif len(item) < self.size:
            item = item + tuple([""] * (self.size - len(item)))
        self.show.append(item)
        self.length = [max(self.length[i], wcswidth(item[i])) for i in range(self.size)]

    def display(self) -> None:
        """
        Displays the information in a formatted manner.
        """
        for row in self.show:
            for j in range(self.size):
                print(f"[{row[j]}" + " " * (self.length[j] - wcswidth(row[j])) + "]", end="")
            print()
        if len(self.show) == 1:
            print(self.empty_msg)


def get_choice_in_options(
    options: Sequence[str],
    within_range_condition: Callable[[int], bool],
    out_range_err_msg: str = "Please enter a valid number.",
    input_not_int_err_msg: str = "Please enter a integer.",
) -> int:
    """
    Displays a list of options and returns the user's choice.
    Args:
        options (Sequence[str]): The list of options to display.
        within_range_condition (Callable[[int], bool]): A function that checks if the input is within range.
        out_range_err_msg (str): The error message to display for out of range input.
        input_not_int_err_msg (str): The error message to display for non-integer input.
    Returns:
        int: The index of the chosen option.
    """
    if isinstance(options, str):
        options = options.split("|")
    show = "".join(f"[{i + 1}.{option.strip()}]" for i, option in enumerate(options)) + ": "

    while True:
        try:
            choice = int(input(show))
            if within_range_condition(choice - 1):
                return choice - 1
            else:
                print(out_range_err_msg)
        except ValueError:
            print(input_not_int_err_msg)


def get_int_input(
    request: str,
    within_range_condition: Callable[[int], bool],
    out_range_err_msg: str = "Please enter a valid number.",
    input_not_int_err_msg: str = "Please enter a integer.",
    stop_condition: Callable[[str], bool] = lambda x: x == "-1",
    stop_flag: int = -1,
) -> int:
    """
    Displays a request to the user and returns an integer input.

    Args:
        request (str): The request message to display.
        within_range_condition (Callable[[int], bool]): A function that checks if the input is within range.
        out_range_err_msg (str): The error message to display for out of range input.
        input_not_int_err_msg (str): The error message to display for non-integer input.
        stop_condition (Callable[[str], bool]): A function that checks if the input is a stop condition.
        stop_flag (int): The value to return if the stop condition is met.

    Returns:
        int: The integer input from the user or the stop flag.
    """
    if not request.endswith(":") and not request.endswith(": "):
        request += ": "
    elif request.endswith(":"):
        request += " "
    while True:
        choice = input(request)
        if stop_condition(choice):
            return stop_flag
        try:
            choice = int(choice)
            if within_range_condition(choice - 1):
                return choice - 1
            else:
                print(out_range_err_msg)
        except ValueError:
            print(input_not_int_err_msg)


def get_range_input(
    request: str,
    within_range_condition: Callable[[int], bool],
    out_range_err_msg: str = "Please enter a valid number.",
    input_not_int_err_msg: str = "Please enter a integer.",
    format_err_msg: str = "Please enter a valid format.",
    stop_condition: Callable[[str], bool] = lambda x: x == "-1",
    stop_flag: tuple[int, ...] = (-1,),
    selection_all_flag: tuple[int, ...] = (-2,),
    flags: tuple[str, ...] = ("-", "~", "all"),  # allowable flags: "-", "~", "all", ","
    discard_err_item: tuple[bool, bool, bool] = (False, False, False),
) -> tuple[int, ...]:
    """
    Displays a request to the user and returns a range of integers based on the input format.

    Args:
        request (str): The request message to display to the user.
        within_range_condition (Callable[[int], bool]): A function that checks if an input number is within valid range.
        out_range_err_msg (str): The error message to display when an input is out of valid range.
        input_not_int_err_msg (str): The error message to display when the input is not an integer.
        format_err_msg (str): The error message to display when the input format is invalid.
        stop_condition (Callable[[str], bool]): A function that checks if the input is a stop condition.
        stop_flag (tuple[int, ...]): The value to return if the stop condition is met.
        selection_all_flag (tuple[int, ...]): The value to return if "all" is selected.
        flags (tuple[str, ...]): The allowable input format flags:
            - "-": Allows range selection using "a-b" format.
            - "~": Allows range selection using "a~b" format.
            - ",": Uses ',' as separator instead of space for multiple selections.
            - "all": Allows returning selection_all_flag to indicate all items are selected.
        discard_err_item (tuple[bool, bool, bool]): Flags to control error handling:
            - [0]: If True, skip out-of-range items instead of aborting.
            - [1]: If True, skip non-integer items instead of aborting.
            - [2]: If True, skip invalid format items instead of aborting.

    Returns:
        tuple[int, ...]: A tuple of integers representing the chosen range. Possible return values:
            - (i1, i2, i3, ...): A tuple of selected integers.
            - stop_flag (default: (-1,)): When the stop condition is met.
            - selection_all_flag(default: (-2,)): When "all" is entered and "all" flag is enabled.
            - Empty tuple (): When no valid selections are made.
    """

    def get_range(t: list[str], result: list[int]) -> int:
        if len(t) != 2:
            print(format_err_msg)
            if not discard_err_item[2]:
                return 2
            return 1
        s, e = t
        if s == "" or e == "":
            print(format_err_msg)
            if not discard_err_item[2]:
                return 2
            return 1
        try:
            s, e = int(s), int(e)
        except ValueError:
            print(input_not_int_err_msg)
            if not discard_err_item[1]:
                return 2
            return 1
        for j in range(s, e + 1):
            if not within_range_condition(j - 1):
                print(out_range_err_msg.format(j))
                if not discard_err_item[0]:
                    return 2
                continue
            result.append(j - 1)
        return 0

    if not request.endswith(":") and not request.endswith(": "):
        request += ": "
    while True:
        choice = input(request)
        if stop_condition(choice):
            return stop_flag
        elif "all" in choice and "all" in flags:
            return selection_all_flag
        result: list[int] = []
        if "," in flags:
            sep = ","
        else:
            sep = " "
        t = -1
        for i in choice.split(sep):
            i = i.strip()
            if "-" in flags and "-" in i:
                t = get_range(i.split("-"), result)
            elif "~" in flags and "~" in i:
                t = get_range(i.split("~"), result)
            else:
                try:
                    i = int(i)
                except ValueError:
                    print(input_not_int_err_msg)
                    if not discard_err_item[1]:
                        t = 2
                        break
                    continue
                if not within_range_condition(i - 1):
                    print(out_range_err_msg.format(i))
                    if not discard_err_item[0]:
                        t = 2
                        break
                    continue
                result.append(i - 1)
            if t == 2:
                break
        if t == 2:
            continue
        return tuple(set(result))


def get_bool_input(request: str, default: Optional[bool] = None, input_err_msg: str = "Please enter 'y' or 'n'.") -> bool:
    """
    Displays a request to the user and returns a boolean input.

    Args:
        request (str): The request message to display.
        default (bool, optional): The default value if the user presses Enter. Defaults to None.
        input_err_msg (str): The error message to display for invalid input.

    Returns:
        bool: The boolean input from the user.
    """
    while True:
        if default is None:
            request = request + "(y/n): "
        elif default:
            request = request + "(Y/n): "
        else:
            request = request + "(y/N): "
        choice = input(request)
        if choice == "" and default is not None:
            return default
        elif choice.lower() in ("y", "yes"):
            return True
        elif choice.lower() in ("n", "no"):
            return False
        else:
            print(input_err_msg)
