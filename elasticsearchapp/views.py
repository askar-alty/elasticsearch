from rest_framework.response import Response
from rest_framework.views import APIView

from elasticsearchapp.search import ElasticSearch
from elasticsearchapp.models import MerchantServices

import requests
import logging
import re
from nltk.stem.snowball import RussianStemmer

# Create your views here.


def clean_text(text):
    if text is not None:
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()


class SearchView(APIView):
    __es = ElasticSearch()

    def post(self, request, *args, **kwargs):
        if request.data:
            data = request.data
            if isinstance(data, dict):
                if data.get('query'):
                    resp = self.__es.search(data['query'])
                    return Response(data={"message": len(resp)}, status=200, template_name="search.html")

    def get(self, request, *args, **kwargs):
        return Response(data={"message": "Search data."}, status=200, template_name="search.html")


class IndexingView(APIView):

    __es = ElasticSearch()

    stemmer = RussianStemmer()

    stop_words = ['установка', 'ремонт']

    def get_terms(self, data):
        line = []
        if isinstance(data, str):
            line.append(data)
        else:
            if isinstance(data, dict):
                for key, val in data.items():
                    line.append(self.get_terms(val))
        return ' '.join(line)

    def parse(self, service):
        line = "{} {} {} {} {} ".format(
            self.get_terms(service.get('allnames')),
            self.get_terms(service.get('altname')),
            self.get_terms(service.get('name')),
            self.get_terms(service.get('srch')),
            self.get_terms(service.get('language')),
        )
        return ', '.join([clean_text(word) for word in re.split(r'[\n;\t,\s]', line) if len(word) and word not in self.stop_words])

    def stem(self, words):
        return ', '.join([row for row in set([self.stemmer.stem(word) for word in words]) if len(row)])

    def get(self, request, *args, **kwargs):

        headers = {'API': 'dictionary',
                   'API_CLIENT': '#######',
                   'API_KEY': '########'}

        resp = requests.post(url='#######', headers=headers, data='["pservices"]')
        data = resp.json()

        logging.debug("Start indexing...")

        MerchantServices.objects.all().delete()

        for book in data['dictionaries']['pservices']['books']:
            for row in book['data']:
                service = MerchantServices()
                service.set_native_id(row.get('id'))
                service.set_parent_id(row.get('parent_id'))
                service.set_top_id(row.get('top_id'))
                service.set_folder(row.get('folder'))
                service.set_edizm_id(row.get('edizm_id')),
                service.set_status(row.get('status')),
                service.set_srch(row.get('srch')),
                service.set_spname(row.get('spname')),
                service.set_typ(row.get('typ')),
                service.set_terms(self.parse(row))
                service.set_stem_terms(self.stem(re.split(r'[\n;\t,\s]', service.get_terms())))
                service.set_allnames(row.get('allnames'))
                service.set_name(clean_text(row.get('name')))
                service.set_popularity(row.get('popularity'))
                service.set_z_id(row.get('z_id'))
                service.save()

        self.__es.bulk_indexing()
        logging.debug("Finish indexing.")
        return Response(data={"message": "Data Indexing!"}, status=201, template_name="indexing.html")

