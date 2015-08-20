from django.conf.urls import patterns, include, url
from django.contrib import admin
from eat_decisive import views
from django.conf import settings
from django.conf.urls.static import static
from . import views
'''
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'eat_decisive.views.index', name='eat_index'),
    url(r'^getdecision/', views.submit_query, name='decision'),
    url(r'^login/', views.login, name='login'),
    url(r'^readdecisive/', views.readdecisive, name='readdecisive'),
    url(r'^goodreadslogin/', views.goodreads_login, name='goodreadslogin'),
    url(r'^readdecisivemember/', views.readdecisivemember, name='readdecisivemember'),
    url(r'^popularbookgenerator/', views.random_popular_book, name='randompopularbook'),
    url(r'^whattoreadnext/', views.random_to_read, name='randomtoread'),
#    url(r'^goodreadslink/', views.goodreads, name='goodreads'),
#    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),

)
'''
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name = 'eat_index'),
    url(r'^getdecision/', views.submit_query, name='decision'),
    url(r'^login/', views.login, name='login'),
    url(r'^readdecisive/', views.readdecisive, name='readdecisive'),
    url(r'^goodreadslogin/', views.goodreads_login, name='goodreadslogin'),
    url(r'^readdecisivemember/', views.readdecisivemember, name='readdecisivemember'),
    url(r'^popularbookgenerator/', views.random_popular_book, name='randompopularbook'),
    url(r'^whattoreadnext/', views.random_to_read, name='randomtoread'),
]

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

