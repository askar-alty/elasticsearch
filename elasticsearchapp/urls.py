from django.conf.urls import url
from elasticsearchapp import views

urlpatterns = [
    url(r'indexing', views.IndexingView.as_view()),
    url(r'search', views.SearchView.as_view()),
]
