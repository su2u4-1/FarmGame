# Farm Game
## 描述 / Description
這是一個簡單的純文字農場小遊戲，玩家可以種植作物或養殖動物來賺取金錢，並用錢來擴張自己的農場。
This is a simple text-based farm game where players can plant crops or raise animals to earn money and use the money to expand their farm.
## 環境 / Environment
- Python 3.8+
- pip install wcwidth
## 檔案結構 / File Structure
```
.
├── README.md           // this file
├── .gitignore          // ignore file
├── archive/            // user archive folder
├── data/
│   ├── animals.json    // animal data
│   ├── crops.json      // crop data
│   ├── items.json      // item data
│   ├── language.json   // support language list
│   └── seed.json       // seed data
├── language/
│   ├── en.json5        // text data in English
│   └── zh-tw.json5     // text data in Chinese(Taiwan)
└── source/
    ├── data.py
    ├── main.py         // program entry point
    ├── player.py
    ├── tools.py
    └── ui.py           // UI functions
```