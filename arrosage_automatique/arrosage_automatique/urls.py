# -*-coding:utf-8-*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gestion_arrosage_automatique.views',
    # Examples:
    # url(r'^$', 'arrosage_automatique.views.home', name='home'),
    # url(r'^arrosage_automatique/', include('arrosage_automatique.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', 'accueil'),
    url(r'parametrage_arrosage/', "parametrage_arrosage"),
    url(r'statistiques_meteorologique/', "statistiques_meteorologiques"),
    url(r'statistiques_arrosage/', "statistiques_arrosages"),
    url(r'rapport_courriel', 'rapport_courriel'),
)
