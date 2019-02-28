from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Course(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	judul = models.CharField(max_length=30)
	thumbnail = models.ImageField(default='mantap.png',blank=True,upload_to='course/')
	kategori = models.CharField(max_length=30)
	harga = models.PositiveIntegerField()
	deskripsi = models.TextField(max_length=300)
	published = models.DateTimeField(auto_now_add=True)
	like = models.PositiveIntegerField(default=0)
	view = models.PositiveIntegerField(default=0)
	share = models.PositiveIntegerField(default=0)
	discount = models.DecimalField(decimal_places=2, max_digits=10,default=0)
	def __str__(self):
		return '{}-{}'.format(self.user, self.judul)

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