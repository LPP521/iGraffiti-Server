from django.conf.urls import url,include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^paste_image/$',csrf_exempt(views.paste_image),name='paste_image'),
    url(r'^wall1/$',csrf_exempt(views.wall1),name='wall1'),
    url(r'^paste/$',csrf_exempt(views.paste),name='paste'),
    url(r'^walldata/$',csrf_exempt(views.walldata),name='walldata'),
    url(r'^createwall/$',csrf_exempt(views.createwall),name='createwall'),
    url(r'^searchwall/$',csrf_exempt(views.searchwall),name='searchwall'),
    url(r'^userinfo/$',csrf_exempt(views.userinfo),name='userinfo'),
    url(r'^searchlist/$',csrf_exempt(views.searchlist),name='searchlist'),
    url(r'^createuser/$',csrf_exempt(views.createuser),name='createuser'),
    url(r'^login/$',csrf_exempt(views.login),name='login'),
    url(r'^addfavo/$',csrf_exempt(views.addfavo),name='addfavo'),
    url(r'^favolist/$',csrf_exempt(views.favolist),name='favolist'),
    url(r'^removefavo/$',csrf_exempt(views.removefavo),name='removefavo'),
    url(r'^walllist/$',csrf_exempt(views.walllist),name='walllist'),
    url(r'^uui/$',csrf_exempt(views.uui),name='uui'),
    url(r'^addnoti/$',csrf_exempt(views.addnoti),name='addnoti'),
    url(r'^removenoti/$',csrf_exempt(views.removenoti),name='removenoti'),
    url(r'^notilist/$',csrf_exempt(views.notilist),name='notilist')
]
