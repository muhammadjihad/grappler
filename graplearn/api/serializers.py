from rest_framework import serializers
from graplearn.models import Course
from akun.api.serializers import UserSerializer

class ListCourseSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	url = serializers.HyperlinkedIdentityField(
			view_name="graplearn-api:detailcourse",
			lookup_field="pk"
		)
	class Meta:
		model = Course
		fields=(
				'user',
				"url",
				'judul',
				'kategori',
				'deskripsi',
			)
	def get_user(self,obj):
		user = {
			"username" : obj.user.username,
			"id" : obj.user.id,
			"level" : obj.user.profile.get_user_level_display()
		}
		return user

class DetailCourseSerializer(serializers.ModelSerializer):
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
				'view',
			)

class UpdateCourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = (
				'judul',
				'kategori',
				'deskripsi',
				'harga'
			)