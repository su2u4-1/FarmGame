# Farm Game
## 描述 / Description
這是一個簡單的純文字農場小遊戲，玩家可以種植作物或養殖動物來賺取金錢，並用錢來擴張自己的農場。
This is a simple text-based farm game where players can plant crops or raise animals to earn money and use the money to expand their farm.
## 環境 / Environment
- Python 3.10+
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
│   ├── en.json         // text data in English
│   └── zh-tw.json      // text data in Chinese(Taiwan)
└── src/
    ├── data.py         // data class
    ├── main.py         // program entry point
    ├── player.py       // player class
    ├── tools.py        // just an empty file now
    └── ui.py           // UI functions
```