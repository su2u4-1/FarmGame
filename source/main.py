import os.path
import json5
import random
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
                    select = input("所選物品id:")
                    try:
                        select = int(select)
                    except:
                        print("輸入非數字")
                        continue
                    for i in player.bag:
                        if DATA["seed"][i]["id"] == select:
                            select = i
                            player.bag[i] -= 1
                            break
                    else:
                        print("所選物品不存在")
                        continue
                    for i in c:
                        v = player.farmland[i]
                        if v.crop != "":
                            f = input(f"邊號{i}農田已經有作物{TEXT[v.crop]}，是否要覆蓋?(Yes/No):")
                            if f != "Yes" and f != "yes" and f != "y" and f != "Y":
                                continue
                            v.weed_appear = False
                            v.bug_number -= random.randrange(v.bug_number)
                            v.weed_appear_prob = max(0, v.weed_appear_prob - random.random())
                        v.crop = select
                        v.growth_time = 0
                        v.ripe = False
                elif option == "2":
                    print(f"你的有機肥料數量: {player.bag["organic_fertilizer"]}, 你的化學肥料數量: {player.bag["chemical_fertilizer"]}")
                    f = input("[1.有機肥料][2.化學肥料]:")
                    if f == "1":
                        f = "organic_fertilizer"
                        t = True
                    elif f == "2":
                        f = "chemical_fertilizer"
                        t = False
                    else:
                        print("輸入錯誤")
                        continue
                    if player.bag[f] < len(c):
                        print(f"你的{TEXT[f]}數量不足")
                        continue
                    player.bag[f] -= len(c)
                    for i in c:
                        v = player.farmland[i]
                        v.soil_fertility += 1
                        v.organic = t
                        if t:
                            v.bug_appear += random() / 10
                        else:
                            v.weed_appear_prob += random() / 10
                elif option == "3":
                    pass
                elif option == "4":
                    pass
                elif option == "5":
                    pass
                elif option == "6":
                    farm_info = table(["編號", "作物", "生長時間", "地力", "新蟲子出現機率", "蟲子數量", "雜草出現機率", "雜草出現", "可收成", "有機"])
                    for i, v in enumerate(player.farmland):
                        if v.crop == "":
                            farm_info.add([i, "Null", "0/0", v.soil_fertility, "0%", 0, "0%", False, False, True])
                        else:
                            farm_info([i, TEXT[v.crop], f"{v.growth_time}/{CROPS[v.crop]["growth_time"]}", v.soil_fertility, f"{round(v.bug_appear*100, 2)}%", v.bug_number, f"{round(v.weed_appear_prob*100, 2)}%", v.weed_appear, v.ripe, v.organic])
                    farm_info.show()
                elif option == "7":
                    break
                else:
                    print("輸入錯誤")

        while True:
            option = input("[1.照顧農田][2.詳細資訊][3.離開]:")
            if option == "1":
                n = input("要照顧的農田編號(可輸入多個數字用空白隔開，輸入all代表全選，可以用a~b來選取一個範圍，輸入-1取消):")
                if n == "-1":
                    continue
                elif n == "all":
                    farm_operate(list(range(len(player.farmland))))
                elif "~" in n:
                    n.replace(" ", "")
                    n = n.split("~", 1)
                    try:
                        n[0] = int(n[0])
                        n[1] = int(n[1])
                    except:
                        print(f"{n[0]}或{n[1]}不是數字")
                        continue
                    if n[0] > n[1]:
                        n[0], n[1] = n[1], n[0]
                    if 0 > n[0] or n[0] >= len(player.farmland):
                        print(f"農田編號{n[0]}不存在")
                        continue
                    if 0 > n[1] or n[1] >= len(player.farmland):
                        print(f"農田編號{n[1]}不存在")
                        continue
                    farm_operate(list(range(n[0], n[1])))
                else:
                    n = n.split()
                    if len(n) == 1:
                        try:
                            n[0] = int(n[0])
                        except:
                            print(f"{n[0]}非數字")
                            continue
                        if 0 <= n[0] < len(player.farmland):
                            c.append(n[0])
                        else:
                            print(f"農田編號{n[0]}不存在")
                            continue
                        farm_operate(0)
                        continue
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
                farm_info = table(["編號", "作物", "生長時間", "地力", "新蟲子出現機率", "蟲子數量", "雜草出現機率", "雜草出現", "可收成", "有機"])
                for i, v in enumerate(player.farmland):
                    if v.crop == "":
                        farm_info.add([i, "Null", "0/0", v.soil_fertility, "0%", 0, "0%", False, False, True])
                    else:
                        farm_info([i, TEXT[v.crop], f"{v.growth_time}/{CROPS[v.crop]["growth_time"]}", v.soil_fertility, f"{round(v.bug_appear*100, 2)}%", v.bug_number, f"{round(v.weed_appear_prob*100, 2)}%", v.weed_appear, v.ripe, v.organic])
                farm_info.show()
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
