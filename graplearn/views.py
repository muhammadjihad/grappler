from django.shortcuts import render, redirect
from .models import Course, VideoCourse, VideoComment
from .forms import CourseForm, VideoCourseForm, VideoCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from collections import deque
from akun.models import Dompet, MyCourse
from django.core.files.storage import  FileSystemStorage

def index(request):

	ListCourse = Course.objects.all()
	ListCourse = ListCourse[::-1]

	context = {
		'judul' : 'graplearn | Learn Everything',
		'jumboTag' : 'Pilih Kursus yang kamu suka!',
		'ListCourse' : ListCourse,
	}

	return render(request,'graplearn/index.html', context)


@login_required
def createCourse(request):

	courseForm = CourseForm

	context = {
		'judul' : 'Upload Courses',
		'jumboTag' : 'Buat Ilmu Kamu Berharga!',
		'courseForm' : courseForm,
	}

	if request.method == 'POST':
		courseForm = CourseForm(request.POST, request.FILES)
		if courseForm.is_valid():
			user = request.user
			judul = courseForm.cleaned_data.get('judul')
			kategori = courseForm.cleaned_data.get('kategori')
			deskripsi = courseForm.cleaned_data.get('deskripsi')
			harga = courseForm.cleaned_data.get('harga')
			thumbnail = courseForm.cleaned_data.get('thumbnail')
			Course.objects.create(
					user = user,
					judul = judul,
					kategori = kategori,
					deskripsi = deskripsi,
					harga = harga,
					thumbnail = thumbnail,
				)
			return redirect ('graplearn:index')

	return render(request, 'graplearn/create.html', context)
	
@login_required
def updateCourse(request, id_update):

	userCourse = Course.objects.get(id = id_update)
	user = userCourse.user
	current_user = User.objects.get(username = request.user.username)

	if current_user != user:
		messages.error(request,'Kamu bukan pembuat dari postingan ini :)')
		return redirect('graplearn:index')

	data = {
		'user' : userCourse.user,
		'judul' : userCourse.judul,
		'deskripsi' : userCourse.deskripsi,
		'kategori' : userCourse.kategori,
		'harga' : userCourse.harga,
		'thumbnail' : userCourse.thumbnail
	}
	updateForm = CourseForm(request.POST or None, instance=userCourse, initial=data)
	context = {
		'judul' : 'Update Form',
		'jumboTag' : 'Update Form',
		'updateForm' : updateForm,
	}

	if request.method == 'POST':
		updateForm = CourseForm(request.POST,request.FILES, instance=userCourse, initial=data)
		if updateForm.is_valid():
			updateForm.save()
			return redirect('graplearn:index')

	return render(request,'graplearn/update.html', context)

@login_required
def userCourses(request):
	userCourses = Course.objects.filter(user = request.user)
	context = {
		'judul' : 'Update Form',
		'jumboTag' : 'Update Form',
		'selfCourses' : userCourses,
	}
	return render(request,'graplearn/usercourses.html', context)

@login_required
def detailCourse(request, id_detail):

	current_user = User.objects.get(id = request.user.id)
	detailCourse = Course.objects.get(id = id_detail)
	userCourses = MyCourse.objects.get(user = request.user)
	userCourses = userCourses.courses.all()
	videoCoursesQuery = VideoCourse.objects.filter(course_id = detailCourse.id)
	videoCourses = []
	for video in videoCoursesQuery:
		videoCourses.append(video)
	print(videoCourses)
	videoComment = []
	for video in videoCourses:
		videoComment.append(VideoComment.objects.filter(videoCourse_id = video.id))
	print(videoComment)
	zipList = zip(videoCourses,videoComment)
	print(zipList)
	# i = 0
	# video_comment = []
	# while i < len(videoCourses):
	# 	video_comment.append((videoCourses[i],videoComment[i]))
	# 	i += 1
	demovid = None
	videoDescript = []
	for desc in videoCourses:
		videoDescript.append(desc.judul)

	try:
		demovid = videoCourses[0]
	except:
		demovid = 'Tidak ada rangkuman Course'

	context = {
		'judul' : 'Detail',
		'jumboTag' : 'Coba Sekarang!',
		'detailCourse' : detailCourse,
		'userCourses' : userCourses,
		'videoCourses' : videoCourses,
		'videoDescript' : videoDescript,
		'videoComment' : videoComment
	}

	if demovid != 'Tidak ada rangkuman Course':
		context['demovid'] = demovid

	if current_user == detailCourse.user:
		context['authUser'] = True

	if not detailCourse in userCourses:
		context['videoCourses'] = None;

	return render(request,'graplearn/detailcourse.html', context)

@login_required
def addVideoCourse(request,id_course):

	course = Course.objects.get(id=id_course)
	videoCourses = VideoCourse.objects.filter(course = course)
	if request.user != course.user:
		messages.error(request,'Kamu gaboleh macem macem ya :)')
		return redirect('home')
	data ={
		'data' : course
	}
	videoCourseForm = VideoCourseForm(initial=data)

	context = {
		'judul' : 'Tambah video kursus',
		'jumboTag' : 'Berikan sedetail mungkin kursus kamu :)',
		'course' : course,
		'videoCourseForm' : videoCourseForm,
		'videoCourses' : videoCourses,
	}
	if request.method == 'POST':
		my_file = request.FILES['video']
		video = VideoCourse.objects.create(
				course = course,
				judul = request.POST.get('judul'),
				video = my_file,
				deskripsi = request.POST.get('deskripsi'),
				referensi = request.POST.get('referensi'),
		)
		video.save()
		VideoComment.objects.create(
				user = request.user,
				videoCourse = video,
				comment = '',
			)

	return render(request,'graplearn/addvideocourse.html', context)

def buy(request,id_course):

	userCourses, created = MyCourse.objects.get_or_create(
		user = request.user
		)
	courseTarget = Course.objects.get(id = id_course)
	dompet, created = Dompet.objects.get_or_create(
			user = request.user
		)
	print(request.user)
	user =  User.objects.get(username = request.user.username)
	userMineCourses = Course.objects.filter(user = user)
	dompetUserCourse,created = Dompet.objects.get_or_create(user = courseTarget.user)
	print(dompetUserCourse)
	for userMineCourse in userMineCourses:
		userCourses.courses.add(userMineCourse)

	coursePrice = courseTarget.harga
	context = {}

	if dompet.uang >= coursePrice:
		if courseTarget not in userCourses.courses.all():
			userCourses.courses.add(courseTarget)
			courseTarget.view += 1
			dompet.uang -= coursePrice
			dompetUserCourse.uang += coursePrice
			courseTarget.save()
			dompetUserCourse.save()
			dompet.save()
		else:
			messages.error(request,'Kamu sudah punya Course ini :)')
	else:
		messages.error(request,'Uangnya kurang :(')

	return redirect('akun:profile')

def commentVideo(request,id_comment):

	video = VideoCourse.objects.get(id = id_comment)
	commentForm = VideoCommentForm

	context = {
		'judul' : 'Komentar Video',
		'jumboTag' : 'Tanyakan sejelas mungkin',
		'video' : video,
		'commentForm' : commentForm

	}

	if request.method == 'POST':
		commentForm = VideoCommentForm(request.POST)
		if commentForm.is_valid():
			messages.success(request,f'Komentar telah dikirim!')
			komentar = commentForm.cleaned_data.get('comment')
			VideoComment.objects.create(
					videoCourse = video,
					user = request.user,
					comment = komentar, 
				)
			return redirect('../../detail/{}'.format(video.course.id))

	return render(request,'graplearn/commentvideo.html', context)