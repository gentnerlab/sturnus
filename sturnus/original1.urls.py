from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from sturnus.api import SubjectResource


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(SubjectResource())

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

    # api urls
    url(r'^api/', include(v1_api.urls)),
)
