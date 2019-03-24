from rest_framework import serializers
from graplearn.models import Course,CourseStatus
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
	course_status = serializers.SerializerMethodField()
	class Meta:
		model = Course
		fields=(
				'user',
				'judul',
				'kategori',
				'deskripsi',
				'harga',
				'published',
				'course_status'
			)
	def get_course_status(self,obj):
		course_status = CourseStatus.objects.get(course=obj)
		course_status = course_status.like.all()
		print(course_status)
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