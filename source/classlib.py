class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.money = 0
        self.bag = {}
        self.corral_n = 1
        self.farmland_n = 5
        self.day = 1

    def show_bag(self) -> None:
        print(self.bag)
