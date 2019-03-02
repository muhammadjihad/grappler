from django.db import models
from django.contrib.auth.models import User


class Postingan(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	judul = models.CharField(max_length=30)
	isi = models.TextField()
	file = models.FileField(upload_to='postingan/',blank=True)
	published = models.DateTimeField(auto_now_add=True)
	like = models.ManyToManyField(User, related_name='postliked')
	share = models.ManyToManyField(User, related_name='postshared')

	def __str__(self):
		return '{}-{}'.format(self.user, self.judul)

class Komentar(models.Model):
 
	postingan = models.ForeignKey(Postingan,on_delete=models.CASCADE, related_name='postingan')
	user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user')
	isi = models.TextField()
	like = models.ManyToManyField(User)

	def __str__(self):
		return '{}-{}'.format(self.id,self.postingan)