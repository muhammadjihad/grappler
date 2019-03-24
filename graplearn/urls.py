from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'graplearn'
urlpatterns=[
	path('createcourse/', views.createCourse, name='createcourse'),
	path('', views.index, name = 'index'),
	re_path(r'^delete/(?P<id_input>[0-9]+)/$',views.deleteCourse, name='deletecourse'),
	re_path(r'^filter/(?P<filter_input>.+)/(?P<judul_input>.+)/$',views.index_filter,name ='filtercourse'),
	re_path(r'^coba/(?P<id_input>[0-9]+)/$',views.cobaDetail,name='cobadetail'),
	re_path(r'^update/(?P<id_update>[0-9]+)/$',views.updateCourse, name='updatecourse'),
	re_path(r'^detail/(?P<id_detail>[0-9]+)/$',views.detailCourse, name='detailcourse'),
	re_path(r'^buy/(?P<id_course>[0-9]+)/$',views.buy, name='buycourse'),
	re_path(r'^addvideocourse/(?P<id_course>[0-9]+)/$',views.addVideoCourse, name='addvideocourse'),
	re_path(r'^videocomment/(?P<id_comment>[0-9]+)/$',views.commentVideo,name='commentvideo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)