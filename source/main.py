import os.path
import json5
from classlib import *


def start() -> None:
    def open_archive() -> Player:
        name = input("存檔名稱(輸入-1取消):")
        if name == "-1":
            return None
        path = os.path.join(root, "archive", name) + ".json5"
        if not os.path.isfile(path):
            print(f"檔案{name}.json5不存在")
            return open_archive()
        with open(path, "r") as f:
            data = json5.load(f)
        player = Player(name)
        player.load(data)
        print(f"玩家{player.name}載入成功")
        return player

    def create_archive() -> Player:
        name = input("玩家名稱(輸入-1取消):")
        if name == "-1":
            return None
        return Player(name)

    print("歡迎遊玩簡單農場")
    while True:
        option = input("[1.開啟存檔][2.建立新存檔][3.離開]:")
        if option == "1":
            player = open_archive()
            if player is None:
                continue
            break
        elif option == "2":
            player = create_archive()
            if player is None:
                continue
            break
        elif option == "3":
            print("遊戲關閉")
            exit()
        else:
            print("輸入錯誤")
    main(player)


def main(player: Player) -> None:
    def other() -> None:
        option = input("[1.更改語言][2.存檔][3.離開遊戲][4.繼續遊戲]:")
        if option == "1":
            while True:
                print("語言列表:")
                for i in DATA["language_list"]:
                    print(i)
                language = input("輸入語言id:")
                if language in DATA["language_list"]:
                    init(root, language)
                    break
                print("輸入錯誤")
        elif option == "2":
            if player.save_archive(root):
                print("存檔成功")
            else:
                print("存檔失敗")
                other()
        elif option == "3":
            f = input("你可能還沒存檔，你確定要離開遊戲嗎?(Yes/No):")
            if f == "Yes" or f == "yes" or f == "y" or f == "Y":
                print("遊戲關閉")
                exit()
            else:
                print("取消")
        elif option != "4":
            print("輸入錯誤")
            other()

    def farmland() -> None:
        def farm_operate(c: list[int]) -> None:
            while True:
                option = input("[1.種植][2.施肥][3.採收/割除][4.除草][5.除蟲][6.資訊][7.離開]:")
                if option == "1":
                    print("你有的種子:")
                    player.bag.show("seed")
                elif option == "2":
                    pass
                elif option == "3":
                    pass
                elif option == "4":
                    pass
                elif option == "5":
                    pass
                elif option == "6":
                    print("[編號][作物][生長時間][地力][新蟲子出現機率][蟲子數量][雜草出現機率][雜草出現]")
                    for i in c:
                        v = player.farmland[i]
                        if v.crop == "":
                            print(f"[{i}][Null][0/0][{v.soil_fertility}][0%][0][0%][False]")
                        else:
                            print(f"[{i}][{TEXT[v.crop]}][{v.growth_time}/{CROPS[v.crop]["growth_time"]}][{v.soil_fertility}][{v.bug_appear*100}%][{v.bug_number}][{v.weed_appear_prob*100}%][{v.weed_appear}]")
                elif option == "7":
                    break
                else:
                    print("輸入錯誤")

        while True:
            option = input("[1.照顧農田][2.詳細資訊][3.離開]:")
            if option == "1":
                n = input("要照顧的農田編號(可輸入多個，用空白隔開，輸入all代表全選):")
                if n == "all":
                    c = list(range(len(player.farmland)))
                    farm_operate(c)
                else:
                    n = n.split()
                    c = []
                    for i in len(n):
                        try:
                            n[i] = int(n[i])
                        except:
                            print(f"{n[i]}非數字")
                            break
                        if 0 <= n[i] < len(player.farmland):
                            c.append(n[i])
                        else:
                            print(f"農田編號{n[i]}不存在")
                            break
                    else:
                        farm_operate(c)
            elif option == "2":
                print("目前農田數:", len(player.farmland))
                print("[編號][作物][生長時間][地力][新蟲子出現機率][蟲子數量][雜草出現機率][雜草出現]")
                for i, v in enumerate(player.farmland):
                    if v.crop == "":
                        print(f"[{i}][Null][0/0][{v.soil_fertility}][0%][0][0%][False]")
                    else:
                        print(f"[{i}][{TEXT[v.crop]}][{v.growth_time}/{CROPS[v.crop]["growth_time"]}][{v.soil_fertility}][{v.bug_appear*100}%][{v.bug_number}][{v.weed_appear_prob*100}%][{v.weed_appear}]")
            elif option == "3":
                return
            else:
                print("輸入錯誤")

    def next_day() -> None:
        print("你回家睡了一覺")
        print("Zzz")
        player.day += 1
        print(f"今天是第{player.day}天")
        player.stamina += player.stamina_recovery_speed
        if player.stamina > player.stamina_max:
            player.stamina = player.stamina_max
        print(f"你的體力回復到了{player.stamina}")
        for i in player.farmland:
            i.next_day()
        for i in player.corral:
            i.next_day()

    print("遊戲開始")
    while True:
        option = input("[1.農田][2.畜欄][3.商店][4.回家][5.其他]:")
        if option == "1":
            farmland()
        elif option == "2":
            pass
        elif option == "3":
            pass
        elif option == "4":
            next_day()
        elif option == "5":
            other()
        else:
            print("輸入錯誤")


if __name__ == "__main__":
    root = os.path.abspath(".")
    if root.endswith("source"):
        root = root[:-7]
    init(root, "zh-tw")
    start()
