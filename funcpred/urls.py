# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import index, GeneAutocomplete, show_gene_search

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^show_gene_search/(?P<gene_search_pk>\d+)/?$', show_gene_search, name='show_gene_search'),
    url(r'^dal/gene/$', GeneAutocomplete.as_view(), name='dal-gene'),
]
