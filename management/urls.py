from django.conf.urls import url
from management import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^add_comic/$', views.add_comic, name='add_comic'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^view_comic_list/$', views.view_comic_list, name='view_comic_list'),
    url(r'^view_comic/detail/$', views.detail, name='detail'),
]
