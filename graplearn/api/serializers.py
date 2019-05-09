from rest_framework import serializers
from graplearn.models import Course,CourseStatus
from akun.api.serializers import UserSerializer
from rest_framework import permissions

class ListCourseSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	url = serializers.HyperlinkedIdentityField(
			view_name="graplearn-api:detailcourse",
			lookup_field="pk"
		)
	user_like=serializers.SerializerMethodField()
	class Meta:
		model = Course
		fields=(
				'user',
				"url",
				'judul',
				'kategori',
				'deskripsi',
				'user_like'
			)
	def get_user(self,obj):
		user = {
			"username" : obj.user.username,
			"id" : obj.user.id,
			"level" : obj.user.profile.get_user_level_display(),
			"foto":obj.user.profile.foto.url,
		}
		return user

	def get_user_like(self,obj):
		course_status = CourseStatus.objects.get(course=obj)
		course_status = course_status.like.all()
		userlike = []
		for user in course_status:
			userlike.append({
				"nama" : user.username,
				"nama_depan" : user.first_name,
				"level" : user.profile.get_user_level_display()
				})
		data = {
			"liked_user" : userlike,
			"like_count" : len(course_status),
		}
		return data


class DetailCourseSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	course_status = serializers.SerializerMethodField()

	class Meta:
		model = Course
		fields=(
				'judul',
				'kategori',
				'deskripsi',
				'harga',
				'published',
				'thumbnail',
				'user',
				'course_status',
			)
		read_only_fields=('course_status','user')
	def get_course_status(self,obj):
		course_status = CourseStatus.objects.get(course=obj)
		course_status = course_status.like.all()
		userlike = []
		for user in course_status:
			userlike.append({
				"nama" : user.username,
				"nama_depan" : user.first_name,
				"level" : user.profile.get_user_level_display()
				})
		data = {
			"liked_user" : userlike,
			"like_count" : len(course_status),
		}
		return data

class UpdateCourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = (
				'judul',
				'kategori',
				'deskripsi',
				'harga'
			)

class PostDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model=Course
		fields='__all__'+'sessionid'
		read_only_fields=('user',)