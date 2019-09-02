CREATE (:criminal:judgment {id:"TPDV,98,重訴,403,20100225,1-01549825-dcaa-4289-8b4d-bbd060277f73", title:"確認債權不存在", caseNum:"98,重訴,403"})
CREATE (:criminal:judgment {id:"TNDM,107,易緝,32,20190121,1-34b5ad0f-e366-4b66-b4e5-84754f4b7c45", title:"賭博等", caseNum: "107,易緝,32"})
CREATE (:criminal:ruling {id:"HLHM,108,聲,7,20190108,1-0c81d8b1-b5a3-48d0-9530-91b666825bd2", title:"聲請定其應執行刑", caseNum: "108,聲,7"})
CREATE (:civil:ruling {id:"KLDV,107,補,621,20190131,1-27338deb-7061-4185-8031-7188dd05984c", title:"返還牌照等", caseNum: "107,補,621"})
CREATE (:admin:judgment {id:"TPBA,107,訴,1145,20190117,2-b306f42d-e141-4232-8f3f-cd5a31c73dbb", title:"巷道爭議", caseNum: "107,訴,1145"})


MATCH (n) DETACH DELETE n

# mongodb

增加 replication 設定
```sh
vim /usr/local/etc/mongod.conf
```

# neo4j
bolt://13.113.158.197:7687
帳號: neo4j
密碼：EibotiG^ZSDXaVxc


# 解析

```sh
nohup python3 -u court.py 4 1 > court_4_1.log &
nohup python3 -u court.py 4 2 > court_4_2.log &
nohup python3 -u court.py 4 3 > court_4_3.log &
nohup python3 -u court.py 4 4 > court_4_4.log &
```
