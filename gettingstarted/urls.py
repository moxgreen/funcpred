from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import funcpred.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', funcpred.views.home, name='index'),
#    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^funcpred/', include('funcpred.urls')),
]
