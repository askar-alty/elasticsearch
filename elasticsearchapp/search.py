import logging
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search, Q, Index

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from elasticsearchapp.models import MerchantServices
from elasticsearchapp.documents import MerchantServicesDocument


connections.create_connection(hosts=['localhost'])


class ElasticSearch:
    __logger = logging
    __client = Elasticsearch()
    __index_name = "merchant_services"
    __doc_type = MerchantServicesDocument
    __index = Index(__index_name)

    def search(self, query):
        self.__logger.debug("in: {}".format(query))
        print("in: {}".format(query))
        s = Search(using=self.__client, index=self.__index_name, doc_type=self.__doc_type)
        # q = Q('match', stem_terms=query)
        q = Q('match', terms=query)
        s = s.query(q)
        responses = s.execute()

        documents = []
        if responses.success():
            for hit in responses.hits:
                documents.append(MerchantServices.objects.get(native_id=hit.native_id))

        self.__logger.debug("out: {}".format(['id: {}, name: {}'.format(doc.get_native_id(), doc.get_name()) for doc in documents]))
        print("out: {}".format(['id: {}, name: {}'.format(doc.get_native_id(), doc.get_name()) for doc in documents]))
        return documents

    def bulk_indexing(self):
        self.__index.delete(ignore=404)
        self.__index.create()
        self.__client.indices.close(index=self.__index_name)
        self.__doc_type.init()
        self.__client.indices.open(index=self.__index_name)

        bulk(client=self.__client, actions=(b.indexing() for b in MerchantServices.objects.all().iterator()))

