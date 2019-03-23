from django.urls import path,re_path
from . import views

app_name='graplearn-api'
urlpatterns=[
	path('',views.ListCourseAPIView.as_view(),name='listcourse'),
	re_path(r'^detail/(?P<pk>[0-9]+)/$',views.DetailCourseAPIView.as_view(),name='detailcourse')

]