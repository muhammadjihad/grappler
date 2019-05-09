from django.urls import path
from . import views

app_name='akun-api'
urlpatterns=[
	path('post/',views.CreateUserAPIView.as_view(), name='createakunapi'),
	path('login/',views.LoginUserAPIView.as_view(),name='login-api'),
	path('logout/',views.LogoutUserAPIView.as_view(),name='logout-api')
]