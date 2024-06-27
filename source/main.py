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
        player.__dict__.update(data)
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

    print("遊戲開始")
    while True:
        option = input("[1.農田][2.畜欄][3.商店][4.回家][5.其他]:")
        if option == "1":
            pass
        elif option == "2":
            pass
        elif option == "3":
            pass
        elif option == "4":
            player.day += 1
            print("你回家睡了一覺")
            print("Zzz")
            print(f"今天是第{player.day}天")
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
