from django.db import models
from django.contrib.auth.models import User
from elasticsearchapp.documents import MerchantServicesDocument


class MerchantServices(models.Model):
    native_id = models.BigIntegerField(default=None)
    parent_id = models.BigIntegerField(default=None)
    top_id = models.BigIntegerField(default=None)
    edizm_id = models.BigIntegerField(default=None)
    status = models.IntegerField(default=None)
    typ = models.CharField(max_length=225, default='')
    spname = models.CharField(max_length=225, default='')

    name = models.TextField()
    allnames = models.TextField()
    folder = models.TextField(default=None)
    srch = models.TextField(default='', blank=True)

    popularity = models.BigIntegerField()
    z_id = models.TextField()

    terms = models.TextField(default='')
    stem_terms = models.TextField(default='')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def get_spname(self):
        return self.spname

    def set_spname(self, spname):
        self.spname = spname

    def get_edizm_id(self):
        return self.edizm_id

    def set_edizm_id(self, edizm_id):
        self.edizm_id = edizm_id

    def get_srch(self):
        return self.srch

    def set_srch(self, srch):
        self.srch = srch

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_typ(self):
        return self.typ

    def set_typ(self, typ):
        self.typ = typ

    def get_parent_id(self):
        return self.parent_id

    def set_parent_id(self, parent_id):
        self.parent_id = parent_id

    def get_top_id(self):
        return self.top_id

    def set_top_id(self, top_id):
        self.top_id = top_id

    def get_folder(self):
        return self.folder

    def set_folder(self, folder):
        self.folder = folder

    def get_terms(self):
        return self.terms

    def set_terms(self, terms):
        self.terms = terms

    def get_stem_terms(self):
        return self.stem_terms

    def set_stem_terms(self, stem_terms):
        self.stem_terms = stem_terms

    def get_native_id(self):
        return self.native_id

    def set_native_id(self, native_id):
        self.native_id = native_id

    def get_allnames(self):
        return self.allnames

    def set_allnames(self, allnames):
        self.allnames = allnames

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_popularity(self):
        return self.popularity

    def set_popularity(self, popularity):
        self.popularity = popularity

    def get_z_id(self):
        return self.z_id

    def set_z_id(self, z_id):
        self.z_id = z_id

    def indexing(self):
        obj = MerchantServicesDocument(
            meta={'id': self.native_id},
            native_id=self.native_id,
            top_id=self.top_id,
            parent_id=self.parent_id,
            spname=self.spname,
            name=self.name,
            allnames=self.allnames,
            folder=self.folder,
            srch=self.srch,
            z_id=self.z_id,
            terms=self.terms,
            stem_terms=self.stem_terms,
            published_from=self.updated
        )
        obj.save()
        return obj.to_dict(include_meta=True)
