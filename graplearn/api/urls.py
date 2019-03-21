from django.urls import path
from . import views

app_name='graplearn-api'
urlpatterns=[
	path('',views.ListCourseAPIView.as_view(),name='listcourse'),

]