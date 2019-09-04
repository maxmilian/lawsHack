MATCH (n) DETACH DELETE n

MATCH (n) RETURN n

# neo4j
[neo4j瀏覽器](http://13.113.158.197:7474/browser/)

bolt://13.113.158.197:7687
帳號: neo4j
密碼：aDeRTYlenTor


# 解析

```sh
# 切割法院跟文書類型
nohup python3 -u court.py 4 1 > court_4_1.log &
nohup python3 -u court.py 4 2 > court_4_2.log &
nohup python3 -u court.py 4 3 > court_4_3.log &
nohup python3 -u court.py 4 4 > court_4_4.log &

# 解析引用判決
nohup python3 -u citation.py 4 1 > citation_4_1.log &
nohup python3 -u citation.py 4 2 > citation_4_2.log &
nohup python3 -u citation.py 4 3 > citation_4_3.log &
nohup python3 -u citation.py 4 4 > citation_4_4.log &

# import 至 neo4j
nohup python3 -u relatedCases.py 8 1 > relatedCases_8_1.log &
nohup python3 -u relatedCases.py 8 2 > relatedCases_8_2.log &
nohup python3 -u relatedCases.py 8 3 > relatedCases_8_3.log &
nohup python3 -u relatedCases.py 8 4 > relatedCases_8_4.log &
nohup python3 -u relatedCases.py 8 5 > relatedCases_8_5.log &
nohup python3 -u relatedCases.py 8 6 > relatedCases_8_6.log &
nohup python3 -u relatedCases.py 8 7 > relatedCases_8_7.log &
nohup python3 -u relatedCases.py 8 8 > relatedCases_8_8.log &
```

# Fulltext search

```sh
CALL db.index.fulltext.createNodeIndex("title", ["CASE"], ["title"])
```

# Property

加入 PageRank Property

```sh
CALL algo.labelPropagation('CASE', 'REFER', 'OUTGOING', {write: true, partitionProperty: "community", weightProperty: "count"})
CALL algo.pageRank('CASE', 'REFER', {write: true, writeProperty:"pagerank"})
CALL algo.betweenness('CASE','REFER', {direction:'out',write:true, writeProperty:'betweenness'})
```
