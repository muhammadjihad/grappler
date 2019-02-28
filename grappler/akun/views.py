from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm
from django.contrib import messages
from .models import Profile, Proyek, Dompet, MyCourse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from graplearn.models import Course, VideoCourse
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
		if userForm.is_valid():
			username = userForm.cleaned_data.get('username')
			nama = userForm.cleaned_data.get('first_name')
			userForm.save()
			user = User.objects.get(username = username)
			Profile.objects.create(
					user = user,
					nama = nama,
					username = username,
					koin = 1,
				)
			messages.success(request,f'Akun dengan username {username} Berhasil dibuat!')
			return redirect('akun:login')

	return render(request,'akun/create.html', context)

@login_required
def profile(request):

	current_user  = User.objects.get(username = request.user.username)
	userCoin, created = Dompet.objects.get_or_create(
		user = request.user
	)
	userProfile = Profile.objects.get(user = request.user)
	userCourse = Course.objects.filter(user = request.user)
	userPrestasi,created = Proyek.objects.get_or_create(
		user = request.user,
	)
	myCourses,created = MyCourse.objects.get_or_create(
		user = current_user
		)
	myCourses = myCourses.courses.exclude(user = request.user)
	users = []
	for course in userCourse:
		users.append(course.user)
	jumlahCourse = len(userCourse)

	context = {
		'judul' : 'Profile',
		'jumboTag' : 'Profile Page',
		'userProfile' : userProfile,
		'userCourse' : userCourse,
		'jumlahCourse' : jumlahCourse,
		'userPrestasi' : userPrestasi,
		'userCoin' : userCoin,
		'users' : users,
		'myCourses' : myCourses
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

def otherprofile(request, user_id):
	user = User.objects.get(id = user_id)
	userProfile = Profile.objects.get(user = user_id)
	userCourse = Course.objects.filter(user = user_id)
	userPrestasi,created = Proyek.objects.get_or_create(
		user = user,
	)
	jumlahCourse = len(userCourse)
	myCourses, created = MyCourse.objects.get_or_create(user = user)
	myCourse = myCourses.courses.exclude(user= user)

	context = {
		'judul' : 'Profile',
		'jumboTag' : 'Profile Page',
		'userProfile' : userProfile,
		'userCourse' : userCourse,
		'jumlahCourse' : jumlahCourse,
		'userPrestasi' : userPrestasi,
		'myCourses' : myCourse,
		'other' : 'other',
	}

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
		formProfile = ProfileForm(request.POST, initial=data,instance=userProfile)
		if formProfile.is_valid():
			formProfile.save()
			return redirect('akun:profile')

	return render(request,'akun/updateprofile.html',context)