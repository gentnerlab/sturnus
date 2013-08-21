from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from tastypie.api import Api


admin.autodiscover()

v1_api = Api(api_name='v1')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sturnus.views.home', name='home'),
    # url(r'^sturnus/', include('sturnus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # grappelli urls
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^broab/', include('broab.urls')),

    # api urls
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', RedirectView.as_view(url='/admin/'), name='go-to-admin')

)
