from django.urls import path, re_path
from . import views

app_name='grappost'
urlpatterns=[
	path('createpost/',views.createpost,name='createpost'),
	path('',views.index,name='index'),
	re_path(r'^like/(?P<id_like>[0-9]+)/$',views.like,name = 'like'),
	re_path(r'^comment/(?P<id_comment>[0-9]+)/$',views.comment, name='comment'),

]