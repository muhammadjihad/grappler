from rest_framework import serializers
from akun.models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields =(
				'username',
				'first_name',
			)