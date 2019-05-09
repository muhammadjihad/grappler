from django.urls import path, re_path
from . import views
from django.contrib.auth import views as authView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'akun'
urlpatterns=[
	path('profile/',views.profile,name = 'profile'),
	path('create/', views.create, name='create'),
	path('usercourses/',views.userCourses,name='usercourses'),
	path('tambahpenghargaan/',views.tambahPenghargaan, name='tambahpenghargaan'),
	path('complainlist/',views.complainList,name='complainlist'),
	path('uploadopeningvideo/',views.uploadOpeningVideo, name='uploadopeningvideo'),
	path('tambahkarya/',views.tambahKarya, name='tambahkarya'),
	path('updateopeningvideo/',views.updateOpeningVideo, name='updateopeningvideo'),
	path('login/', authView.LoginView.as_view(template_name = 'akun/login.html'), name = 'login'),
	path('logout/', authView.LogoutView.as_view(template_name = 'akun/logout.html'), name = 'logout'),
	path('tukarkoin/',views.tukarKoin,name='tukarkoin'),
	path('listpesan/',views.listPesan,name='listpesan'),
	re_path(r'^method/(?P<method>.+)/(?P<course_id>[0-9]+)/$', views.akunmethod, name = 'akunmethod'),
	re_path(r'^users/(?P<user_id>[0-9]+)/$',views.otherprofile, name='otherprofile'),
	re_path(r'^detailpesan/(?P<id_sender_user>[0-9]+)/$',views.detailPesan, name='detailpesan'),
	re_path(r'^deleteprestasi/(?P<prestasi>[\w]+)/(?P<id_prestasi>[0-9]+)/$',views.deletePrestasi, name='deleteprestasi'),
	re_path(r'^updateprofile/(?P<profile_id>[0-9]+)/$',views.updateprofile,name='updateprofile'),
	re_path(r'^friend/(?P<operation>[\w]+)/(?P<id_input>[0-9]+)/$',views.friendToggle,name='friendtoggle'),
	re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)