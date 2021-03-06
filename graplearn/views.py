from django.shortcuts import render, redirect, reverse
from .models import Course, VideoCourse, VideoComment, CourseStatus, CourseAdvertisment
from .forms import CourseForm, VideoCourseForm, VideoCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from collections import deque
from akun.models import Dompet, MyCourse, Profile, Friend, Complaining, ExpiredCourse
from django.core.files.storage import  FileSystemStorage
from django.core.paginator import Paginator
from akun.forms import ComplainingForm

def index(request):
	courseAds = CourseAdvertisment.CourseAdsAll()
	ListCourse = Course.getAllCourseByLevel()
	course_status = []
	for course in ListCourse:
		each_course = CourseStatus.objects.get_or_create(course=course)
		user_liked_course = each_course[0].like.all()
		course_status.append(
			(user_liked_course,course)
			)
	course_status = Paginator(course_status,15)
	page = request.GET.get('page')
	course_status = course_status.get_page(page)
	context = {
		'judul' : 'graplearn | Learn Everything',
		'jumboTag' : 'Pilih Kursus yang kamu suka!',
		'ListCourse' : course_status,
		'courseAds' :courseAds,
	}

	if request.method == 'POST':
		filter_input = request.POST['filter']
		judul_input = request.POST['textinput']
		kategori_input = request.POST['choiceinput']
		direct_input = None

		if filter_input == '':
			filter_input = 'all'

		if judul_input =='' and kategori_input == '':
			direct_input = 'time'
		if judul_input == '' and kategori_input != '':
			direct_input = kategori_input
		if kategori_input == '' and judul_input != '':
			direct_input = judul_input

		return redirect(reverse("graplearn:filtercourse",
			kwargs={
			"filter_input":filter_input,
			"judul_input":direct_input,
			}))

	return render(request,'graplearn/index.html', context)

def index_filter(request,filter_input,judul_input):

	ListCourse = None
	course_status = []
	courseAds = None

	def arrangement():
		for course in ListCourse:
			each_course = CourseStatus.objects.get_or_create(course=course)
			user_liked_course = each_course[0].like.all()
			course_status.append(
				(user_liked_course,course)
				)

	if filter_input == "judul":
		ListCourse = Course.objects.filter(judul__contains=judul_input)
		courseAds = CourseAdvertisment.objects.filter(course__judul__contains=judul_input)
	elif filter_input == "user_level":
		ListCourse = Course.filterCourseByLevel(judul_input)
		courseAds = CourseAdvertisment.filterCourseAdsByLevel(judul_input)
	elif filter_input == "kategori":
		ListCourse = Course.objects.filter(kategori__contains=judul_input)
		courseAds = CourseAdvertisment.objects.filter(course__kategori__contains=judul_input)
	elif filter_input == "published":
		ListCourse = Course.objects.all().order_by("-id")
		courseAds = CourseAdvertisment.objects.all().order_by("-id")
	else:
		return redirect("graplearn:index")
	arrangement()
	course_status = Paginator(course_status,14)
	page = request.GET.get('page')
	course_status = course_status.get_page(page)

	context = {
		'judul' : 'graplearn | Learn Everything',
		'jumboTag' : 'Pilih Kursus yang kamu suka!',
		'ListCourse' : course_status,
		'all' : 'all',
		'courseAds' :courseAds,
	}

	if len(courseAds) == 0:
		context['courseAdsNull'] = 'courseAdsNull'

	if request.method == 'POST':
		filter_input = request.POST['filter']
		judul_input = request.POST['textinput']
		kategori_input = request.POST['choiceinput']
		direct_input = None

		if filter_input == '':
			filter_input = 'all'

		if judul_input =='' and kategori_input == '':
			direct_input = 'time'
		elif judul_input == '' and kategori_input != '':
			direct_input = kategori_input
		elif kategori_input == '' and judul_input != '':
			direct_input = judul_input
		return redirect(reverse("graplearn:filtercourse",
			kwargs={
			"filter_input":filter_input,
			"judul_input":direct_input,
			}))

	return render(request,'graplearn/index.html', context)

@login_required
def createCourse(request):

	courseForm = CourseForm
	userCourses = MyCourse.objects.get(user = request.user)
	current_user = User.objects.get(id=request.user.id)
	current_user_courses = Course.objects.filter(user=request.user)


	context = {
		'judul' : 'Upload Courses',
		'jumboTag' : 'Buat Ilmu Kamu Berharga!',
		'courseForm' : courseForm,
	}

	def save_new_course():
		new_course = courseForm.save(commit=False)
		new_course.user = request.user
		new_course.save()
		userProfile = Profile.objects.get(user = request.user)
		userProfile.gainExp(35)
		CourseStatus.objects.create(
				course = new_course
			)
		userCourses.courses.add(new_course)
		return redirect ('graplearn:index')

	if request.method == 'POST':
		courseForm = CourseForm(request.POST, request.FILES)
		if courseForm.is_valid():
			if current_user.profile.user_level == '1' and len(current_user_courses) < 8:
				save_new_course()
			elif current_user.profile.user_level == '2' and len(current_user_courses) < 17:
				save_new_course()
			elif current_user.profile.user_level == '3' and len(current_user_courses) < 25:
				save_new_course()
			elif current_user.profile.user_level == '4' and len(current_user_courses) < 35:
				save_new_course()
			elif current_user.profile.user_level == '5' and len(current_user_courses) < 45:
				save_new_course()
			elif current_user.profile.user_level == '6':
				save_new_course()
			else:
				messages.info(request,f'Kamu tidak memenuhi persyaratan maksimum unggah kursus berdasarkan level, Tetap Semangat! :)')
			

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
def detailCourse(request, id_detail):
	try:
		ExpiredCourse.expired_course_method(request.user.id)
	except:
		pass
	current_user = User.objects.get(id = request.user.id)
	detailCourse = Course.objects.get(id = id_detail)
	userCourses = MyCourse.objects.get(user = request.user)
	userCourses = userCourses.courses.all()
	videoCoursesQuery = VideoCourse.objects.filter(course_id = detailCourse.id)
	videoCourses = []
	for video in videoCoursesQuery:
		videoCourses.append(video)
	videoComment = []
	for video in videoCourses:
		videoComment.append(VideoComment.objects.filter(videoCourse_id = video.id))
	zipList = zip(videoCourses,videoComment)
	demovid = None
	videoDescript = []
	for desc in videoCourses:
		videoDescript.append(desc.judul)
	try:
		demovid = videoCourses[0]
	except:
		demovid = 'Tidak ada rangkuman Course'
	print(videoCourses)

	context = {
		'judul' : 'Detail',
		'jumboTag' : 'Coba Sekarang!',
		'detailCourse' : detailCourse,
		'userCourses' : userCourses,
		'videoCourses' : videoCourses,
		'videoDescript' : videoDescript,
		'videoComment' : videoComment,
		'videoCoursesCount' : len(videoCourses)
	}

	try:
		context['complainCourse'] = Complaining.objects.filter(course=detailCourse).count()
		sender_user=[]
		for complain in Complaining.objects.filter(course=detailCourse):
			sender_user.append(complain.sender_user)
		if request.user in sender_user:
			context['alreadycomplain'] = 'Kamu sudah komplain'
			print('reach')
	except:
		pass

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
	videoCourseForm = VideoCourseForm(request.POST or None, request.FILES or None)

	context = {
		'judul' : 'Tambah video kursus',
		'jumboTag' : 'Berikan sedetail mungkin kursus kamu :)',
		'course' : course,
		'videoCourseForm' : videoCourseForm,
		'videoCourses' : videoCourses,
	}
	if request.method == 'POST':
		videoCourseForm = VideoCourseForm(request.POST or None, request.FILES or None)
		if videoCourseForm.is_valid():
			video = videoCourseForm.save(commit=False)
			video.course = course
			video.save()
			VideoComment.objects.create(
					user = request.user,
					videoCourse = video,
					comment = '',
				)

	return render(request,'graplearn/addvideocourse.html', context)

@login_required
def updateVideoCourse(request,id_video):
	videoCourse = VideoCourse.objects.filter(id = id_video)
	course = Course.objects.get(id=videoCourse[0].course.id)
	if request.user != videoCourse[0].course.user:
		messages.error(request,'Kamu gaboleh macem macem ya :)')
		return redirect('home')
	data = {
		'course' : videoCourse[0].course,
		'video' : videoCourse[0].video,
		'judul' : videoCourse[0].judul,
		'deskripsi' : videoCourse[0].deskripsi,
		'published' : videoCourse[0].published,
		'referensi' : videoCourse[0].referensi,
	}
	videoCourseForm = VideoCourseForm(request.POST or None, instance=videoCourse[0], initial=data)
	context = {
		'judul' : 'Tambah video kursus',
		'jumboTag' : 'Berikan sedetail mungkin kursus kamu :)',
		'course' : course,
		'videoCourseForm' : videoCourseForm,
		'videoCourses' : videoCourse,
	}
	if request.method == 'POST':
		videoCourseForm = VideoCourseForm(request.POST, request.FILES, instance=videoCourse[0])
		if videoCourseForm.is_valid():
			videoCourseForm.save()

	return render(request,'graplearn/addvideocourse.html', context)

@login_required
def deleteVideoCourse(request,id_video):
	video = VideoCourse.objects.get(id=id_video)
	if video.course.user != request.user:
		return redirect("akun:profile")
	else:
		video.delete()
		return redirect(reverse("graplearn:detailcourse",kwargs={
				'id_detail':video.course.id
			}))

@login_required
def buy(request,id_course):

	userCourses, created = MyCourse.objects.get_or_create(
		user = request.user
		)
	courseTarget = Course.objects.get(id = id_course)
	dompet, created = Dompet.objects.get_or_create(
			user = request.user
		)
	user =  User.objects.get(username = request.user.username)
	userMineCourses = Course.objects.filter(user = user)
	dompetUserCourse,created = Dompet.objects.get_or_create(user = courseTarget.user)
	for userMineCourse in userMineCourses:
		userCourses.courses.add(userMineCourse)

	coursePrice = courseTarget.harga
	context = {}
	courseStatus = CourseStatus.objects.get(course = courseTarget)
	if dompet.uang >= coursePrice:
		if courseTarget not in userCourses.courses.all():
			ExpiredCourse.objects.create(
					buyed_course = courseTarget,
					buyed_user = request.user,
				)
			userCourses.courses.add(courseTarget)
			courseTarget.view += 1
			courseTarget.user.profile.gainExp(50*int(courseTarget.user.profile.user_level))
			user.profile.gainExp(60*int(user.profile.user_level))
			dompet.uang -= coursePrice
			dompetUserCourse.uang += coursePrice
			courseTarget.save()
			courseStatus.student.add(request.user)
			dompetUserCourse.save()
			dompet.save()
		else:
			messages.error(request,'Kamu sudah punya Course ini :)')
	else:
		messages.error(request,'Uangnya kurang :(')

	return redirect('akun:profile')

@login_required
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
			return redirect(reverse("graplearn:detailcourse",kwargs={
					"id_detail" : video.course.id
				}))

	return render(request,'graplearn/commentvideo.html', context)

@login_required
def deleteCourse(request,id_input):

	course = Course.objects.get(id = id_input)
	if request.user != course.user:
		return redirect("graplearn:index")
	else:
		course.user.profile.un_gainExp(35*int(course.user.profile.user_level))
		course.delete()
	return redirect("graplearn:index")

@login_required
def like(request,operation,id_input):
	CourseStatus.operation(user = request.user,method=operation,id_input=id_input)
	if operation == 'like':
		request.user.profile.gainExp(5*int(request.user.profile.user_level))
	return redirect("graplearn:index")

@login_required
def complain(request,id_input):

	sender_courses = MyCourse.objects.get(user=request.user)
	sender_courses = sender_courses.courses.all()
	this_course = Course.objects.get(id=id_input)
	receiver_user = User.objects.get(user = request.user)
	if not this_course in sender_courses:
		return redirect(reverse("graplearn:detailcourse",kwargs={
				"id_detail" : id_input,
			}))
	latest_complain = Complaining.objects.filter(
		course=this_course,
		)
	latest_users_complain = []
	for complain in latest_complain:
		latest_users_complain.append(complain.sender_user)
	complainForm = ComplainingForm
	context={
		'judul' : 'Komplain',
		'sender_courses' : sender_courses,
		'complainForm' : complainForm
	}

	if request.method == 'POST':
		complainForm = ComplainingForm(request.POST)
		if request.user in latest_users_complain:
			Complaining.objects.get(sender_user=request.user).delete()
		if complainForm.is_valid():
			new_complain = complainForm.save(commit=False)
			new_complain.sender_user = request.user
			new_complain.course = this_course
			new_complain.receiver_user = this_course.user
			new_complain.save()
			receiver_user.profile.gainExp(25*int(receiver_user.profile.user_level))
			return redirect(reverse("graplearn:detailcourse",kwargs={
				"id_detail" : id_input,
			}))
		

	return render(request,'graplearn/complain.html',context)