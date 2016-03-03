# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import RealtaListView,RealtaMarkersView

urlpatterns = [
    url(r'^$', RealtaListView.as_view(), name='realta-list'),
    url(r'^api/markers.tab$', RealtaMarkersView.as_view(), name='marker-list'),
]
