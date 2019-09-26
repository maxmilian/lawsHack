# 台灣判決引用網路

## 前言

因為參加第一屆台灣[法律科技黑客松](https://hackathon.lawsnote.com/)，在主辦單位辛苦的媒合下，有了法律背景的隊友。其實這次比賽不是以往的黑客松一個週末要做出一個作品，而是給定約2個月的時間，讓隊伍有機會好好的把成品展現。

在這2個月的時間內，其實跟隊友討論過數次題目，因為我跟隊友工作也挺忙，所以進度頗慢。直到快要比賽前一週，才真的快速趕工生出此作品，真心覺得還不錯。

[成果網站](http://legalhack.tech/)

## 開放資料

主辦單位有開發他們有解析的資料，不過這次比賽我們沒有使用他們的解析資料，而是直接使用司法院的[開放資料](http://data.judicial.gov.tw/)，裁判文書的範圍從 1996 年開始，持續更新。目前導入的文書一共有 1400萬篇文書左右。


## 資料處理

資料處理大概分以下3個步驟，(使用 python 處理)

- 導入裁判文書到 mongod (`import.py`)
- 使用 regular expression 找出有引用的裁判文書，並且更新 mongodb (`citation.py`)
- 把引用的資料再導入到 neo4j (`relatedCaes.py`)

```sh
# parse citation
nohup python3 -u citation.py 8 1 > citation_8_1.log &
nohup python3 -u citation.py 8 2 > citation_8_2.log &
nohup python3 -u citation.py 8 3 > citation_8_3.log &
nohup python3 -u citation.py 8 4 > citation_8_4.log &
nohup python3 -u citation.py 8 5 > citation_8_5.log &
nohup python3 -u citation.py 8 6 > citation_8_6.log &
nohup python3 -u citation.py 8 7 > citation_8_7.log &
nohup python3 -u citation.py 8 8 > citation_8_8.log &

# import to neo4j
nohup python3 -u relatedCases.py 8 1 > relatedCases_8_1.log &
nohup python3 -u relatedCases.py 8 2 > relatedCases_8_2.log &
nohup python3 -u relatedCases.py 8 3 > relatedCases_8_3.log &
nohup python3 -u relatedCases.py 8 4 > relatedCases_8_4.log &
nohup python3 -u relatedCases.py 8 5 > relatedCases_8_5.log &
nohup python3 -u relatedCases.py 8 6 > relatedCases_8_6.log &
nohup python3 -u relatedCases.py 8 7 > relatedCases_8_7.log &
nohup python3 -u relatedCases.py 8 8 > relatedCases_8_8.log &
```

## neo4j

這次使用 [neo4j](https://neo4j.com/) 算是一個新的技術組合，之前我也沒有玩過，算是趁這次黑客松來熟悉 neo4j。

網路上已經很多教學說明，這裡簡單列出幾個。

- [Neo4j 官網](https://neo4j.com/)
- [Neo4j Console](https://console.neo4j.org/) 直接online demo，可以下指令
- [Neo4j Sandbox](https://neo4j.com/sandbox-v2/) Neo4j沙盒，裡面有一些現成的資料和neo4j，可以直接啟用來玩，有時間限制

### 常用指令

```sh
# 登出
:server disconnect

# 查詢節點
MATCH (n) RETURN n

# 刪除所有節點與關聯
MATCH (n) DETACH DELETE n
```

### Fulltext search

```sh
CALL db.index.fulltext.createNodeIndex("title", ["CASE"], ["title"])

CALL db.index.fulltext.queryNodes("title", "'殺人'") YIELD node, score
RETURN node.title, score
```

### Property

加入 PageRank Property

```sh
CALL algo.labelPropagation('CASE', 'REFER', 'OUTGOING', {write: true, partitionProperty: "community", weightProperty: "count"})

CALL algo.pageRank('CASE', 'REFER', {write: true, writeProperty:"pagerank"})

CALL algo.betweenness('CASE','REFER', {direction:'out',write:true, writeProperty:'betweenness'})
```


## 前端網頁

這邊的前端頁面我找了很久，覺得沒有很適合的，所以還是直接使用 [jekyllBasic模板](https://github.com/bchetty/jekyllBasic)，最後的[成果網站](http://legalhack.tech/)。

使用 ruby v2.6.4 並用以下方式開發、編譯

```sh
# 開發
bundle exec jekyll serve

# 編譯
bundle exec jekyll build
```

# 協作
此專案由 Max Hsu maxmilian@gmail.com 完成，

歡迎協作，請使用 GitHub issue 以及 Pull Request 功能來協作。
