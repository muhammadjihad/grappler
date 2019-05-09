from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Postingan(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	judul = models.CharField(max_length=30)
	isi = models.TextField()
	file = models.FileField(upload_to='postingan/',blank=True, null=True)
	published = models.DateTimeField(auto_now_add=datetime.now)
	like = models.ManyToManyField(User, related_name='postliked')
	share = models.ManyToManyField(User, related_name='postshared')
	PILIHAN_KATEGORI_POST = (
			('1','Mencari'),
			('2','Promo'),
			('3','Bertanya'),
		)
	kategori_post = models.CharField(max_length=1,choices=PILIHAN_KATEGORI_POST)

	def __str__(self):
		return '{}-{}'.format(self.user, self.judul)

class Komentar(models.Model):
 
	postingan = models.ForeignKey(Postingan,on_delete=models.CASCADE, related_name='postingan')
	user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user')
	isi = models.TextField()
	like = models.ManyToManyField(User)
	published = models.DateTimeField(auto_now_add=True)
	helping = models.BooleanField(default=False)

	def __str__(self):
		return '{}-{}'.format(self.id,self.postingan)