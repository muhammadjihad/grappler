from django.db import models
from django.contrib.auth.models import User
from operator import itemgetter
from django.urls import reverse
from datetime import timedelta, date
# Create your models here.


class Course(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	judul = models.CharField(max_length=30)
	thumbnail = models.ImageField(default='mantap.png',blank=True,upload_to='course/')
	kategori = models.CharField(max_length=30)
	harga = models.PositiveIntegerField()
	deskripsi = models.TextField(max_length=300)
	published = models.DateTimeField(auto_now_add=True)
	discount = models.DecimalField(decimal_places=2, max_digits=10,default=0)
	def __str__(self):
		return '{}-{}'.format(self.user, self.judul)

	@classmethod
	def getDetailCourse(cls,id):
		return cls.objects.get(id = id)
		
	@classmethod
	def getAllCourse(cls):
		return cls.objects.all()

	@classmethod
	def getAllCourseByLevel(cls):
		courses = cls.objects.all()
		list_courses = []
		for course in courses:
			list_courses.append((int(course.user.profile.user_level),course.id))
		list_courses = sorted(list_courses, reverse=True)
		ready_course = []
		for course in list_courses:
			ready_course.append(cls.objects.get(id = course[1]))
		return ready_course

	@classmethod
	def filterCourseByLevel(cls, filter):
		courses = cls.objects.all()
		list_courses = []
		for course in courses:
			if course.user.profile.get_user_level_display() == filter.capitalize():
				list_courses.append(course)
		return list_courses

class CourseAdvertisment(models.Model):
	course = models.OneToOneField(Course, on_delete=models.CASCADE)
	start = models.DateField(auto_now_add=True)
	duration=models.PositiveIntegerField(default=30)

	def __str__(self):
		return self.course.judul

	def expired_ads_system(self):
		date_expired = self.start + timedelta(days=self.duration)
		if date.today() >= date_expired:
			self.delete()
	
	@classmethod
	def CourseAdsAll(cls):
		courses = cls.objects.all()
		list_course=[]
		for course in courses:
			course.expired_ads_system()
			list_course.append(course)
		return list_course
	@classmethod
	def filterCourseAdsByLevel(cls, filter):
		courses = cls.objects.all()
		list_courses = []
		for course in courses:
			if course.course.user.profile.get_user_level_display() == filter.capitalize():
				date_expired=course.start+timedelta(days=course.duration)
				print(date_expired)
				if date.today() > date_expired:
					course.delete()
				else:
					list_courses.append(course)
		return list_courses


class CourseStatus(models.Model):
	course = models.OneToOneField(Course, on_delete=models.CASCADE)
	like = models.ManyToManyField(User, blank=True, related_name='like')
	student = models.ManyToManyField(User, blank=True, related_name='view')

	def __str__(self):
		return self.course.judul

	@classmethod
	def operation(cls,user,method,id_input):
		if method == "like":
			course = Course.objects.get(id=id_input)
			course_status = cls.objects.get_or_create(
					course = course
				)
			if not user in course_status[0].like.all():
				course_status[0].like.add(user)
			else:
				course_status[0].like.remove(user)
		return reverse("graplearn:index")

	@classmethod
	def getCourseLike(cls,course):
		like=0
		userCourse = cls.objects.filter(course=course)
		for course in userCourse:
			user_like = course.like.all()
			like += len(user_like)
		return like

class VideoCourse(models.Model):

	course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True)
	video = models.FileField(upload_to='coursevideos/')
	judul = models.CharField(max_length=40)
	deskripsi = models.TextField(max_length=300, blank=True)
	published = models.DateTimeField(auto_now_add=True)
	referensi = models.TextField(blank=True)
	alat_atau_bahan = models.TextField(blank=True)

	def __str__(self):
		return '{}.{}'.format(self.id, self.course)


class VideoComment(models.Model):

	videoCourse = models.ForeignKey(VideoCourse,on_delete=models.CASCADE)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
	comment 	= models.TextField(blank=True)
	published 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.user,self.videoCourse)

class ComplainCourse(models.Model):

	sender_user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	complain = models.TextField()
	solusi = models.TextField()

	def __str__(self):
		return self.course.judul