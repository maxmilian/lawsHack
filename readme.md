CREATE (:V {JID:"TPDV,98,重訴,403,20100225,1-01549825-dcaa-4289-8b4d-bbd060277f73", JTITLE:"確認債權不存在", JYEARCASENO:"98,重訴,403"})
CREATE (:M {JID:"TNDM,107,易緝,32,20190121,1-34b5ad0f-e366-4b66-b4e5-84754f4b7c45", JTITLE:"賭博等", JYEARCASENO: "107,易緝,32"})
CREATE (:M {JID:"HLHM,108,聲,7,20190108,1-0c81d8b1-b5a3-48d0-9530-91b666825bd2", JTITLE:"聲請定其應執行刑", JYEARCASENO: "108,聲,7"})
CREATE (:V {JID:"KLDV,107,補,621,20190131,1-27338deb-7061-4185-8031-7188dd05984c", JTITLE:"返還牌照等", JYEARCASENO: "107,補,621"})
CREATE (:A {JID:"TPBA,107,訴,1145,20190117,2-b306f42d-e141-4232-8f3f-cd5a31c73dbb", JTITLE:"巷道爭議", JYEARCASENO: "107,訴,1145"})

MATCH (n) DETACH DELETE n

MATCH (n) RETURN n

# mongodb

增加 replication 設定
```sh
vim /usr/local/etc/mongod.conf
```

# neo4j
[neo4j瀏覽器](http://13.113.158.197:7474/browser/)

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

# 修改數據格式

```sh
db.TW_case.find({JYEAR:{$type:2}}).forEach(function(obj) {
  obj.JYEAR = new NumberInt(obj.JYEAR);
  db.TW_case.save(obj);
});


db.TW_case.find({JNO:{$type:2}}).forEach(function(obj) {
    obj.JNO = new NumberInt(obj.JNO);
    db.TW_case.save(obj);
});
```
