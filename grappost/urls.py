from django.urls import path, re_path
from . import views

app_name='grappost'
urlpatterns=[
	path('createpost/',views.createpost,name='createpost'),
	path('',views.index,name='index'),
	re_path(r'^filter/(?P<parameter>[\w]+)/(?P<judul_post>[\w]+)/$',views.index_all_filter,name='index_all'),
	re_path(r'^like/(?P<id_like>[0-9]+)/$',views.like,name = 'like'),
	re_path(r'^comment/(?P<id_comment>[0-9]+)/$',views.comment, name='comment'),
	re_path(r'^deletepost/(?P<id_post>[0-9]+)/$',views.deletePost, name='deletepost'),
	re_path(r'^deletecomment/(?P<id_komen>[0-9]+)/$',views.deleteKomen, name='deletecomment'),
	re_path(r'^helpingcomment/(?P<operation>[\w-]+)/(?P<id_comment>[0-9]+)/$',views.help_comment,name='helpingcomment')
]