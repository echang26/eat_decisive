from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name = 'eat_index'),
    url(r'^getdecision/', views.submit_query, name='decision'),
    url(r'^login/', views.login, name='login'),
    url(r'^readdecisive/', views.readdecisive, name='readdecisive'),
    url(r'^goodreadslogin/', views.goodreads_login, name='goodreadslogin'),
#    url(r'^readdecisivemember/\?oauth_token', views.goodreads_redirect, name='goodreadsredirect'),
    url(r'^readdecisivemember/', views.readdecisivemember, name='readdecisivemember'),
    url(r'^popularbookgenerator/', views.random_popular_book, name='randompopularbook'),
    url(r'^whattoreadnext/', views.random_to_read, name='randomtoread'),
    url(r'^readalternative/', views.read_alternative, name='readalternative'),
    url(r'^readalternativeresult/', views.read_result, name='readalternativeresult'),
]

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'eat_decisive.views.handler404'
handler500 = 'eat_decisive.views.handler500'
