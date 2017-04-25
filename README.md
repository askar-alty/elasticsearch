1 Установка elasticsearch
-
   - ``wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.3.1.tar.gz``
   - ``shasum elasticsearch-5.3.1.tar.gz ``
   - ``tar -xzf elasticsearch-5.3.1.tar.gz``
   - ``cd elasticsearch-5.3.1/ ``
   - ``./elasticsearch-5.3.1/bin/elasticsearch``

2 Проверка работы elasticsearch
- 
   - ``curl -X GET http://localhost:9200``

    ответ: 
    
    {
      "name" : "CChMeuS",
      "cluster_name" : "elasticsearch",
      "cluster_uuid" : "ZEXRR6iqQrWLhh7MltZceQ",
      "version" : {
        "number" : "5.3.1",
        "build_hash" : "5f9cf58",
        "build_date" : "2017-04-17T15:52:53.846Z",
        "build_snapshot" : false,
        "lucene_version" : "6.4.2"
      },
      "tagline" : "You Know, for Search"
    }

