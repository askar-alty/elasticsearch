from django.utils import timezone
from elasticsearch_dsl import DocType, Text, Date, Integer, Keyword
from elasticsearch_dsl import analyzer, tokenizer, token_filter


term_analyzer = analyzer('term_analyzer',
                             tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=5),
                             filter=[
                                 "standard",
                                 "lowercase",
                                 "snowball",
                                 token_filter(
                                     'custom_filter',
                                     type='stop',
                                     stopwords=['установка', 'ремонт']
                                 )
                             ],
                             char_filter=["html_strip"]
                         )


class MerchantServicesDocument(DocType):
    native_id = Integer()
    parent_id = Integer()
    top_id = Integer()
    spname = Text(analyzer='snowball')
    name = Text(analyzer='snowball')
    allnames = Text(analyzer='snowball')
    folder = Text(analyzer='snowball')
    srch = Text(analyzer='snowball')
    z_id = Text(analyzer='snowball')
    terms = Text(analyzer=term_analyzer, fields={'raw': Keyword()})
    stem_terms = Text(analyzer=term_analyzer, fields={'raw': Keyword()})
    published_from = Date()

    class Meta:
        index = 'merchant_services'

    def is_published(self):
        return timezone.now() < self.published_from
