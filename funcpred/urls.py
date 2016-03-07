# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import home, GeneAutocomplete, FunctionAutocomplete, show_gene_search, show_function_search, gene_search, function_search

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^gene_search$', gene_search, name='gene_search'),
    url(r'^function_search$', function_search, name='gene_search'),
    url(r'^_gene_search/(?P<gene_search_pk>\d+)/?$', show_gene_search, name='show_gene_search'),
    url(r'^show_function_search/(?P<function_search_pk>\d+)/?$', show_function_search, name='show_function_search'),
    url(r'^dal/gene/$', GeneAutocomplete.as_view(), name='dal-gene'),
    url(r'^dal/function/$', FunctionAutocomplete.as_view(), name='dal-function'),
]
