# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import index, GeneAutocomplete

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^dal/gene/$', GeneAutocomplete.as_view(), name='dal-gene'),
]
