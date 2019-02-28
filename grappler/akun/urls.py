from django.urls import path, re_path
from . import views
from django.contrib.auth import views as authView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'akun'
urlpatterns=[
	path('profile/',views.profile,name = 'profile'),
	path('create/', views.create, name='create'),
	path('login/', authView.LoginView.as_view(template_name = 'akun/login.html'), name = 'login'),
	path('logout/', authView.LogoutView.as_view(template_name = 'akun/logout.html'), name = 'logout'),
	re_path(r'^method/(?P<method>.+)/(?P<course_id>[0-9]+)/$', views.akunmethod, name = 'akunmethod'),
	re_path(r'^users/(?P<user_id>[0-9]+)/$',views.otherprofile, name='otherprofile'),
	re_path(r'^updateprofile/(?P<profile_id>[0-9]+)/$',views.updateprofile,name='updateprofile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)