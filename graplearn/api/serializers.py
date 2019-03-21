from rest_framework import serializers
from graplearn.models import Course
from akun.api.serializers import UserSerializer

class ListCourseSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Course
		fields=(
				'user',
				'judul',
				'kategori',
				'deskripsi',
				'harga',
				'published',
				'like',
				'view'
			)