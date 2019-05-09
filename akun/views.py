from django.shortcuts import render, redirect, reverse
from .forms import UserForm, PesanForm, ComplainingForm ,ProfileForm, OpeningVideoForm, TestimoniForm, PenghargaanForm, KaryaForm
from django.contrib import messages
from .models import Profile, Proyek, Dompet, MyCourse, Friend, ExpiredCourse, Karya, Pesan
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from graplearn.models import Course, VideoCourse, CourseStatus
from grappost.models import Postingan
from akun.models import OpeningVideo, Testimoni, Complaining, Friend, TukarKoin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from grappler.settings import EMAIL_HOST_USER
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import random, operator
import time
import os
from datetime import date,timedelta
# Create your views here.

def create(request):

	userForm = UserForm

	context ={
		'judul' : 'Buat Profil',
		'jumboTag' : 'Make Your Own Account',
		'userForm' : userForm,
	}

	if request.method == 'POST':
		userForm = UserForm(request.POST)
		try:
			if request.POST.get('email') == User.objects.get(email=request.POST.get('email')).email:
				messages.warning(request,'email sudah digunakan')
				return redirect("akun:create")
			if request.POST.get('username') == User.objects.get(email=request.POST.get('username')).username:
				messages.warning(request,'username sudah digunakan')
				return redirect("akun:create")
		except:
			pass
		if userForm.is_valid():
			new_user = userForm.save(commit=False)
			new_user.is_active = False
			new_user.save()
			current_site = get_current_site(request)
			mail_subject = "Aktivasi akun Flixnote"
			pesan = render_to_string('akun/aktivasi.html',{
					'user' : new_user,
					'domain' : current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
					'token': account_activation_token.make_token(new_user),
				})
			send_mail(
			    mail_subject,
			    pesan,
			    EMAIL_HOST_USER,
			    [new_user.email],
			    fail_silently=False,
			)
			username = userForm.cleaned_data.get('username')
			nama = userForm.cleaned_data.get('first_name')
			user = User.objects.get(username = username)
			Profile.objects.create(
					user = user,
					nama = nama,
					username = username,
					koin = 1,
				)
			messages.success(request,f'Akun dengan username {username} Berhasil dibuat!')
			messages.warning(request,f'Silahkan konfirmasi akun lewat email yang anda Masukkan :)')
			return redirect('akun:login')

	return render(request,'akun/create.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,f'akun dengan username {user.username} berhasil diaktivasi, silakan login :)')
        return redirect('akun:login')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def profile(request):

	current_user  = User.objects.get(username = request.user.username)
	userCoin, created = Dompet.objects.get_or_create(
		user = request.user
	)
	userKarya = Karya.get_all_class_extension(request.user)
	userProfile = Profile.objects.get(user = request.user)
	userCourse = Course.objects.filter(user = request.user)
	userPrestasi = Proyek.objects.filter(user=request.user)
	myCourses,created = MyCourse.objects.get_or_create(
		user = current_user
		)
	myCourses = myCourses.courses.exclude(user = request.user)
	users = []
	for course in userCourse:
		users.append(course.user)
	jumlahCourse = len(userCourse)
	userPost = Postingan.objects.filter(user = current_user)[::-1]
	testimoni = Testimoni.objects.filter(receiver_user = request.user).order_by("-sender_user__profile__user_level")[:4]
	userOpeningVideo, created = OpeningVideo.objects.get_or_create(
		user = request.user
	)
	students=0
	like=0
	postingan=len(userPost)
	lovepost=0
	complain_count=len(Complaining.objects.filter(receiver_user=request.user))
	for course,post in zip(userCourse,userPost):
		students += (CourseStatus.objects.get(course=course).student.count())
		like += (CourseStatus.objects.get(course=course).like.count())
		lovepost += post.like.count()
	complains=[]
	for course in userCourse:
		complains.append(len(Complaining.objects.filter(course=course)))
	courseStatus=[]
	for course,complain in zip(userCourse,complains):
		courseStatus.append((course,complain))
	print(userCoin.uang)
	uang = '{:,.2f}'.format(userCoin.uang)
	print(uang)
	context = {
		'judul' : 'Profile',
		'jumboTag' : 'Profile Page',
		'userProfile' : userProfile,
		'userCourse' : courseStatus,
		'userKarya' : userKarya,
		'jumlahCourse' : jumlahCourse,
		'userPrestasi' : userPrestasi,
		'userCoin' : uang,
		'users' : users,
		'myCourses' : myCourses,
		'userPost' : userPost,
		'openingVideo' : userOpeningVideo,
		'testimoni' :testimoni,
		'students' : students,
		'like' : like,
		'postingan' : postingan,
		'lovepost' : lovepost,
		'complain':complain_count,
		'course':len(userCourse)
	}
	
	if request.user.profile == userProfile:
		context['settingbutton'] = 'setting'

	return render(request, 'akun/profile.html', context)

@login_required
def akunmethod(request, method, course_id):
	if method == 'like':
		course = Course.objects.get(id = course_id)
		course.like += 1
		course.save()
	elif method == 'view':
		course = Course.objects.get(id = course_id)
		course.view += 1
		course.save()
	elif method == 'share':
		course = Course.objects.get(id = course_id)
		course.share += 1
		course.save()
	else:
		return redirect('graplearn:index')
	return redirect('graplearn:index')

@login_required
def otherprofile(request, user_id):
	user = User.objects.get(id = user_id)
	if request.user == user:
		return redirect("akun:profile")
	userProfile = Profile.objects.get(user = user_id)
	userCourse = Course.objects.filter(user = user_id)
	userPrestasi = Proyek.objects.filter(user=user)
	jumlahCourse = len(userCourse)
	myCourses, created = MyCourse.objects.get_or_create(user = user)
	myCourse = myCourses.courses.exclude(user= user)
	userPost = Postingan.objects.filter(user = user_id)
	testimoni = Testimoni.objects.filter(receiver_user = user)[:4]
	userOpeningVideo, created = OpeningVideo.objects.get_or_create(
		user = user
	)
	current_user_friend = Friend.objects.get_or_create(
			current_user = User.objects.get(id=request.user.id)
		)
	testimoniForm = TestimoniForm
	students=0
	like=0
	postingan=len(userPost)
	lovepost=0
	complain_count=len(Complaining.objects.filter(receiver_user=user))
	for course,post in zip(userCourse,userPost):
		students += (CourseStatus.objects.get(course=course).student.count())
		like+=CourseStatus.getCourseLike(course=course)
		lovepost += post.like.count()
	complains=[]
	for course in userCourse:
		complains.append(len(Complaining.objects.filter(course=course)))
	courseStatus=[]
	for course,complain in zip(userCourse,complains):
		courseStatus.append((course,complain))

	context = {
		'current_user' : request.user,
		'judul' : 'Profile',
		'jumboTag' : 'Profile Page',
		'userProfile' : userProfile,
		'userCourse' : courseStatus,
		'jumlahCourse' : jumlahCourse,
		'userFriend':current_user_friend[0],
		'userPrestasi' : userPrestasi,
		'myCourses' : myCourse,
		'other' : 'other',
		'userPost' : userPost,
		'testimoni':testimoni,
		'openingVideo' : userOpeningVideo,
		'testimoniForm' : testimoniForm,
		'students' : students,
		'like' : like,
		'postingan' : postingan,
		'lovepost' : lovepost,
		'complain':complain_count,
		'course' : len(userCourse)
	}

	user_testimoni = Testimoni.objects.filter(receiver_user=user)
	sender_user = []
	for user in user_testimoni:
		sender_user.append(user.sender_user)
	if request.user in sender_user:
		context['alreadytest'] = 'alreadytest'

	user = User.objects.get(id = user_id)
	if request.method == 'POST':
		testimoniForm = TestimoniForm(request.POST)
		if testimoniForm.is_valid():
			new_testimoni = testimoniForm.save(commit=False)
			new_testimoni.sender_user = request.user
			new_testimoni.receiver_user = User.objects.get(id=user_id)
			new_testimoni.save()
			receiver_profile = Profile.objects.get(user=user)
			sender_profile = Profile.objects.get(user=request.user)
			receiver_profile.gainExp(20*int(sender_profile.user_level))
			return redirect(reverse("akun:otherprofile",kwargs={
					'user_id':user_id
				}))

	return render(request, 'akun/profile.html', context)

@login_required
def updateprofile(request,profile_id):

	userProfile = Profile.objects.get(id = profile_id)

	if request.user.profile != userProfile:
		return redirect('akun:profile')
	data = {
		'nama' : userProfile.nama,
		'waktu_lahir' : userProfile.waktu_lahir,
		'bio' : userProfile.bio,
		'foto' : userProfile.foto,
		'alamat' : userProfile.alamat,
		'thumbnail' : userProfile.thumbnail,
		'deskripsi_kanal' : userProfile.deskripsi_kanal,
		'kontak' : userProfile.kontak
	}
	formProfile = ProfileForm(initial=data,instance = userProfile)

	context = {
		'judul' : 'Update Profile Kamu!',
		'jumboTag' : 'Update Profile',
		'userProfile' : userProfile,
		'formProfile' : formProfile
	}

	if request.method == 'POST':
		formProfile = ProfileForm(request.POST,request.FILES, initial=data,instance=userProfile)
		if formProfile.is_valid():
			formProfile.save()
			return redirect('akun:profile')

	return render(request,'akun/updateprofile.html',context)

@login_required
def uploadOpeningVideo(request):
	videoForm = OpeningVideoForm(request.POST or None, request.FILES or None)

	context ={
		'judul' : 'Buat Opening Video',
		'jumboTag' : 'Make Your Own Account',
		'videoForm' : videoForm,
	}

	if request.method == 'POST':
		try:
			OpeningVideo.objects.get(user=request.user).delete()
		except:
			pass
		videoForm = OpeningVideoForm(request.POST,request.FILES)
		if videoForm.is_valid():
			new_opening_video = videoForm.save(commit=False)
			new_opening_video.user = request.user
			new_opening_video.save()
			return redirect('akun:profile')

	return render(request,'akun/uploadopeningvideo.html', context)

@login_required
def updateOpeningVideo(request):

	openingVideo = OpeningVideo.objects.get(user = request.user)

	if openingVideo.user != request.user:
		return redirect('akun:profile')
	data = {
		'video':openingVideo.video,
		'judul':openingVideo.judul
	}
	videoForm = OpeningVideoForm(initial=data,instance = openingVideo)

	context={
		'judul':'Ubah Opening Video',
		'videoForm':videoForm,
	}

	if request.method == 'POST':
		videoForm = OpeningVideoForm(request.POST,request.FILES)
		if videoForm.is_valid():
			openingVideo.delete()
			new_opening_video = videoForm.save(commit=False)
			new_opening_video.user = request.user
			new_opening_video.user.id = request.user.id
			new_opening_video.save()
			return redirect("akun:profile")

	return render(request,'akun/uploadopeningvideo.html', context)

@login_required
def tambahPenghargaan(request):
	formPenghargaan = PenghargaanForm

	context={
		'judul' : 'Tambah penghargaan',
		'formPenghargaan' : formPenghargaan
	}

	if request.method == 'POST':
		formPenghargaan = PenghargaanForm(request.POST,request.FILES)
		if formPenghargaan.is_valid():
			new_penghargaan = formPenghargaan.save(commit=False)
			new_penghargaan.user = request.user
			new_penghargaan.save()
			return redirect('akun:profile')

	return render(request,'akun/tambahpenghargaan.html',context)

@login_required
def tambahKarya(request):
	karyaForm = KaryaForm

	context={
		'judul' : 'Tambah Karya',
		'karyaForm' : karyaForm,
	}

	if request.method == 'POST':
		karyaForm = KaryaForm(request.POST,request.FILES)
		if karyaForm.is_valid():
			new_karya = karyaForm.save(commit=False)
			new_karya.user = request.user
			new_karya.save()
			return redirect("akun:profile")

	return render(request,'akun/karya.html',context)

@login_required
def deletePrestasi(request, prestasi, id_prestasi):
	if prestasi == 'karir':
		karir = Proyek.objects.get(id = id_prestasi)
		if request.user == karir.user:
			karir.delete()
	if prestasi == 'karya':
		karya = Karya.objects.get(id = id_prestasi)
		if request.user == karya.user:
			karya.delete()
	return redirect("akun:profile")

@login_required
def userCourses(request):
	try:
		available_course = ExpiredCourse.expired_course_method(request.user.id)
	except:
		pass
	userCourse = MyCourse.objects.get(user=request.user)
	courses =userCourse.courses.exclude(user=request.user)
	list_course=[]
	try:
		for course in courses:
			course_start=ExpiredCourse.objects.get(buyed_course=course, buyed_user=request.user).start_date
			date_expired=course_start+timedelta(days=30)
			days_left=date_expired-date.today()
			list_course.append((course,days_left.days))
	except:
		pass
	context={
		'judul' : 'Ini Kursus yang kamu beli',
		'courses' : list_course,
	}
	return render(request,'akun/usercourses.html',context)

@login_required
def friendToggle(request,operation,id_input):
	user_target = User.objects.get(id=id_input)
	profile_target = Profile.objects.get(user=user_target)
	current_user_friend = Friend.objects.get(current_user=request.user)
	if operation == 'follow':
		current_user_friend.users.add(user_target)
		current_user_friend.save()
		profile_target.gainExp(15*int(profile_target.user_level))
	if operation == 'unfollow':
		current_user_friend.users.remove(user_target)
		current_user_friend.save()
		profile_target.un_gainExp(15*int(profile_target.user_level))
	return redirect(reverse("akun:otherprofile",kwargs={'user_id':id_input}))

@login_required
def complainList(request):
	costumer_complains = Complaining.objects.filter(receiver_user=request.user)
	context={
		'judul' : 'Komplain',
		'complains' : costumer_complains
	}
	return render(request,'akun/complain.html',context)

@login_required
def tukarKoin(request):
	userKoin = Dompet.objects.get(user=request.user)
	if userKoin.uang == 0:
		messages.success(request,f'kamu belum memiliki koin untuk ditukarkan')
		return redirect('akun:profile')
	local_time = time.asctime(time.localtime())
	share_profit = None
	user_percentage = None
	user_money = None
	biaya_admin = None
	if userKoin.user.profile.user_level == '1':
		share_profit = '5%'
		user_percentage = '95%'
		biaya_admin = userKoin.uang*0.05
		biaya_admin_rupiah = 'Rp {:,.2f}'.format(biaya_admin)
		user_money = userKoin.uang - biaya_admin
		user_money = 'Rp {:,.2f}'.format(user_money)
	elif userKoin.user.profile.user_level == '2':
		share_profit = '7.5%'
		user_percentage = '92.5%'
		biaya_admin = userKoin.uang*0.075
		biaya_admin_rupiah = 'Rp {:,.2f}'.format(biaya_admin)
		user_money = userKoin.uang - biaya_admin
		user_money = 'Rp {:,.2f}'.format(user_money)
	elif userKoin.user.profile.user_level == '3':
		share_profit = '10%'
		user_percentage = '90%'
		biaya_admin = userKoin.uang*0.1
		biaya_admin_rupiah = 'Rp {:,.2f}'.format(biaya_admin)
		user_money = userKoin.uang - biaya_admin
		user_money = 'Rp {:,.2f}'.format(user_money)
	elif userKoin.user.profile.user_level == '4':
		share_profit = '12.5%'
		user_percentage = '87.5%'
		biaya_admin = userKoin.uang*0.125
		biaya_admin_rupiah = 'Rp {:,.2f}'.format(biaya_admin)
		user_money = userKoin.uang - biaya_admin
		user_money = 'Rp {:,.2f}'.format(user_money)
	elif userKoin.user.profile.user_level == '5':
		share_profit = '15%'
		user_percentage = '85%'
		biaya_admin = userKoin.uang*0.15
		biaya_admin_rupiah = 'Rp {:,.2f}'.format(biaya_admin)
		user_money = userKoin.uang - biaya_admin
		user_money = 'Rp {:,.2f}'.format(user_money)
	elif userKoin.user.profile.user_level == '6':
		share_profit = '17.5%'
		user_percentage = '82.5%'
		biaya_admin = userKoin.uang*0.175
		biaya_admin_rupiah = 'Rp {:,.2f}'.format(biaya_admin)
		user_money = userKoin.uang - biaya_admin
		user_money = 'Rp {:,.2f}'.format(user_money)
	nomor_verifikasi = random.randint(1000,9999)
	current_site = get_current_site(request)
	mail_subject = "Verifikasi Tukar Koin Flixnote"
	pesan = render_to_string('akun/tukarkoin.html',{
			'koin' : userKoin,
			'koin_show' : '{:,.2f}'.format(userKoin.uang),
			'domain' : current_site.domain,
			'nomor_verifikasi' : nomor_verifikasi,
			'share_profit' : share_profit,
			'user_money' : user_money,
			'biaya_admin' : biaya_admin_rupiah,
			'user_percentage' : user_percentage,
			'local_time':local_time
		})
	send_mail(
			mail_subject,
			pesan,
			EMAIL_HOST_USER,
			[request.user.email, EMAIL_HOST_USER],
			fail_silently=False,
		),
	TukarKoin.objects.create(
			user = request.user
		)
	messages.success(request,f'Penukaran Berhasil, silahkan cek email untuk dapatkan nomor verifikasi dan hubungi CS kami!')
	userKoin.uang = 0
	userKoin.save()
	return redirect("akun:profile")

def listPesan(request):
	pesan = Pesan.objects.filter(receiver_user=request.user)
	sender_user_id = pesan.values_list('sender_user',flat=True).distinct()
	front_pesan=[]
	for sender_id in sender_user_id:
		front_pesan.append(
				Pesan.objects.filter(sender_user__id = sender_id).last()
			)
	front_pesan = sorted(front_pesan,key=operator.attrgetter('waktu_kirim'),reverse=True)
	context={
		'judul' : 'Pesan Masuk',
		'jumboTag' : 'Pesan Masuk',
		'pesan_masuk' : front_pesan
	}
	return render(request,'akun/list_pesan.html',context)

def detailPesan(request, id_sender_user):
	sender_user = User.objects.get(id=id_sender_user)
	pesan_masuk = Pesan.objects.filter(sender_user__id=id_sender_user).filter(receiver_user__id=request.user.id)
	pesan_keluar = Pesan.objects.filter(sender_user__id=request.user.id).filter(receiver_user__id=id_sender_user)
	semua_pesan=[]
	pesanForm = PesanForm
	for masuk in pesan_masuk:
		semua_pesan.append(masuk)
		masuk.read = True
		masuk.save()
	for keluar in pesan_keluar:
		semua_pesan.append(keluar)
	semua_pesan = sorted(semua_pesan,key=operator.attrgetter('waktu_kirim'), reverse=True)
	context={
		'judul' : 'Kirim Pesan ke User ini',
		'semua_pesan':semua_pesan,
		'sender_user':sender_user,
		'pesanForm' : pesanForm
	}

	if request.method == "POST":
		pesanForm = pesanForm(request.POST,request.FILES)
		if pesanForm.is_valid():
			new_pesan = pesanForm.save(commit=False)
			new_pesan.sender_user=request.user
			new_pesan.receiver_user=sender_user
			new_pesan.save()
			return redirect(reverse("akun:detailpesan",kwargs={
					'id_sender_user':id_sender_user
				}))

	return render(request,'akun/pesan.html',context)