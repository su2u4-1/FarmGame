from typing import Callable, Sequence

from wcwidth import wcswidth  # type: ignore


class Display_info:
    def __init__(self, title: Sequence[object] | str) -> None:
        """
        Initializes the Display_info class with a title.

        Args:
            title (list[object] | str): The title to display.
        """
        if isinstance(title, str):
            title = tuple(title.split("|"))
        else:
            title = tuple(str(t) for t in title)
        self.show = [title]
        self.size = len(title)
        self.length: list[int] = [wcswidth(t) for t in title]

    def add(self, item: Sequence[object]) -> None:
        """
        Adds an item to the display.
        Args:
            item (Sequence[object]): The item to add.
        Raises:
            ValueError: If the length of the item exceeds the title length.
        """
        if isinstance(item, str):
            item = tuple(item.split("|"))
        else:
            item = tuple(str(i) for i in item)
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


def display_option_and_get_input(
    options: Sequence[str],
    out_range_condition: Callable[[int], bool],
    out_range_err_msg: str = "Please enter a valid number.",
    input_not_int_err_msg: str = "Please enter a integer.",
) -> int:
    """
    Displays a list of options and returns the user's choice.
    Args:
        options (Sequence[str]): The list of options to display.
        out_range_condition (Callable[[int], bool]): A function that checks if the input is out of range.
        out_range_err_msg (str): The error message to display for out of range input.
        input_not_int_err_msg (str): The error message to display for non-integer input.
    Returns:
        int: The index of the chosen option.
    """
    for i, option in enumerate(options):
        print(f"[{i + 1}.{option}]", end="")

    while True:
        try:
            choice = int(input(": "))
            if out_range_condition(choice):
                print(out_range_err_msg)
            else:
                return choice - 1
        except ValueError:
            print(input_not_int_err_msg)


def display_request_and_get_int_input(
    request: str,
    out_range_condition: Callable[[int], bool],
    out_range_err_msg: str = "Please enter a valid number.",
    input_not_int_err_msg: str = "Please enter a integer.",
    stop_condition: Callable[[str], bool] = lambda x: x == "-1",
    stop_flag: int = -1,
) -> int:
    """
    Displays a request to the user and returns an integer input.

    Args:
        request (str): The request message to display.
        out_range_condition (Callable[[int], bool]): A function that checks if the input is out of range.
        out_range_err_msg (str): The error message to display for out of range input.
        input_not_int_err_msg (str): The error message to display for non-integer input.
        stop_condition (Callable[[str], bool]): A function that checks if the input is a stop condition.
        stop_flag (int): The value to return if the stop condition is met.

    Returns:
        int: The integer input from the user or the stop flag.
    """
    while True:
        choice = input(request)
        if stop_condition(choice):
            return stop_flag
        try:
            choice = int(choice)
            if out_range_condition(choice):
                print(out_range_err_msg)
            else:
                return choice
        except ValueError:
            print(input_not_int_err_msg)


def display_message(message: str) -> None:
    """
    Displays a message to the user.

    Args:
        message (str): The message to display.
    """
    print(message)


def display_info(title: Sequence[object] | str, *items: Sequence[object]) -> None:
    """
    Displays information about a title and its items.

    Args:
        title (list[object] | str): The title to display.
        item (Sequence[object]): The items to display.

    Raises:
        ValueError: If the length of an item exceeds the length of the title.
    """
    display = Display_info(title)
    for item in items:
        display.add(item)
    display.display()
