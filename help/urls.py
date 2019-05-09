from django.urls import path
from . import views

app_name='help'
urlpatterns=[
	path('', views.index, name='index'),
	path('isikoin/',views.koin, name='isikoin'),
	path('tukarkoin/',views.tukarkoin, name='tukarkoin'),
	path('sistemlevel/',views.sistemlevel, name='sistemlevel'),
	path('iklankursus/',views.iklankursus,name='iklankursus'),
	path('paketiklan/',views.paketiklan,name='paketiklan')
]