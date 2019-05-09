from django.db import models
from django.contrib.auth.models import User
from graplearn.models import Course
from datetime import date, timedelta
import os
# Create your models here.

class Profile(models.Model):

	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	nama 			= models.CharField(max_length=25)
	PILIHAN_STATUS  = (
			('Reguler', 'Reguler'),
			('Premium', 'Premium'),
		)
	status			= models.CharField(max_length=25, choices=PILIHAN_STATUS) # ini nanti hapus
	username		= models.CharField(max_length=25) #ini hapus aja
	waktu_lahir 	= models.DateField(auto_now_add=True)
	bio				= models.TextField(max_length=300, blank=True)
	foto 			= models.ImageField(default='mantap.jpg',upload_to='profilepicture/',blank=True)
	koin			= models.PositiveIntegerField() # ini nanti dibuat class sendiri aja
	alamat 			= models.CharField(max_length=50, blank=True)
	thumbnail 		= models.ImageField(blank=True, upload_to='profilebanner/')
	deskripsi_kanal = models.TextField(blank=True)
	kontak			= models.PositiveIntegerField(blank=True,default=0)
	PILIHAN_LEVEL	= (
			('1','Novice'),
			('2','Beginner'),
			('3','Competent'),
			('4','Expert'),
			('5','Master'),
			('6','Legend'),
		)
	user_level	= models.CharField(max_length=1,choices=PILIHAN_LEVEL,default='1')
	user_exp = models.PositiveIntegerField(default=0)
	verified = models.BooleanField(default=False)
	twitter_url = models.URLField(blank=True)
	facebook_url = models.URLField(blank=True)
	linkedin_url = models.URLField(blank=True)
	instagram_url = models.URLField(blank=True)
	whatsapp_account = models.CharField(blank=True, max_length=15)
	line_account = models.CharField(blank=True, max_length=15)

	def __str__(self):
		return '{}'.format(self.nama)


	def leveling(self):
		if self.user_exp < 0:
			self.user_exp = 0
		elif self.user_exp < 1000:
			self.user_level = '1'
			self.save()
		elif self.user_exp < 7000:
			self.user_level = '2'
			self.save()
		elif self.user_exp < 35000:
			self.user_level = '3'
			self.save()
		elif self.user_exp < 200000:
			self.user_level = '4'
			self.save()
		elif self.user_exp < 1000000:
			self.user_level = '5'
			self.save()
		else:
			self.user_level = '6'
			self.save()

	def gainExp(self, input_exp):
		self.user_exp += input_exp
		self.leveling()
		self.save()
	def un_gainExp(self, input_exp):
		self.user_exp -= input_exp
		self.leveling()
		self.save()
	class Meta:
		ordering = ["user_level"]

class OpeningVideo(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	video = models.FileField(upload_to='openingprofilevideo/')
	judul = models.CharField(max_length=25)

	def __str__(self):
		return self.user.username

class Proyek(models.Model):

	user 			= models.ForeignKey(User, on_delete=models.CASCADE)
	prestasi	 	= models.CharField(max_length=35,blank=True)
	waktu 			= models.DateField(auto_now_add=True)
	deskripsi 		= models.TextField(blank=True)
	file 			= models.FileField(blank=True)

	def __str__(self):
		return '{}-{}'.format(self.user, self.prestasi)

class Karya(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	judul = models.CharField(max_length=55)
	file = models.FileField(upload_to='userkarya/', blank=True)
	keterangan = models.TextField()

	def __str__(self):
		return "{} - {}".format(self.user.username,self.judul)

	@classmethod
	def get_all_class_extension(cls,user_filter):
		all_class = cls.objects.filter(user=user_filter)
		nama_extension=[]
		for karya in all_class:
			nama_file, extension = os.path.splitext(karya.file.name)
			nama_extension.append(
					(karya, extension)
				)
		return nama_extension

class Pesan(models.Model):

	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pesan_sender_user')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pesan_receiver_user')
	pesan = models.TextField()
	file = models.FileField(blank=True, upload_to='user_message/')
	read = models.BooleanField(default=False)
	waktu_kirim = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{} to {}".format(self.sender_user.username, self.receiver_user.username)


class Dompet(models.Model):

	user 			= models.ForeignKey(User, on_delete=models.CASCADE)
	uang 			= models.PositiveIntegerField(default=0)

	def __str__(self):
		return '{}-{}'.format(self.user,self.uang)

class MyCourse(models.Model):

	user 			= models.ForeignKey(User, on_delete=models.CASCADE)
	courses 		= models.ManyToManyField(Course, blank=True)

	def __str__(self):
		return '{}'.format(self.user)

class ExpiredCourse(models.Model):
	buyed_user = models.ForeignKey(User,on_delete=models.CASCADE)
	buyed_course = models.ForeignKey(Course,on_delete=models.CASCADE)
	start_date = models.DateField(auto_now_add=True)
	expired = models.BooleanField(default=False)

	def __str__(self):
		return self.buyed_course.judul

	@classmethod
	def expired_course_method(cls,id_user):
		courses = MyCourse.objects.get(user_id=id_user)
		user_courses = courses.courses.exclude(user=courses.user)
		for course in user_courses:
			expiring_course = cls.objects.get(buyed_course=course,buyed_user=courses.user)
			if date.today() > expiring_course.start_date+timedelta(days=30):
				expiring_course.expired = True
				expiring_course.save()
				courses.courses.remove(course)

class Testimoni(models.Model):

	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver_user')
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender_user')
	testimoni = models.TextField()
	published = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{} to {}".format(self.sender_user.username, self.receiver_user.username)

class Friend(models.Model):

	users 			= models.ManyToManyField(User)
	current_user 	= models.OneToOneField(User,on_delete=models.CASCADE, null=True, related_name='owner')

	@classmethod
	def make_friend(cls,new_friend,current_user):
		friend, created = cls.objects.get_or_create(
				current_user = current_user
			)
		friend.users.add(new_friend)

	@classmethod
	def remove_friend(cls,new_friend,current_user):
		friend, created = cls.objects.get_or_create(
				current_user = current_user
			)
		friend.users.remove(new_friend)

	def __str__(self):
		return self.current_user.username

class Complaining(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='receiver_complain_course')
	sender_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender_complain_user')
	receiver_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_complain_user')
	komplain = models.TextField()
	saran = models.TextField()
	published = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{} to {}'.format(self.sender_user.username,self.receiver_user.username)

	@classmethod
	def getUserComplain(cls,course_id):
		return cls.objects.filter(id=course_id)

class TukarKoin(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	waktu_dilakukan = models.DateTimeField(auto_now_add=True, editable=False)
	selesai = models.BooleanField(default=False)

	def __str__(self):
		return '{} - {}'.format(self.user.username, self.user.email)