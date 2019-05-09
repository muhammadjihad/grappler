from rest_framework import serializers
from akun.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields =(
				'username',
				'first_name',
			)

class CreateUserSerializer(serializers.ModelSerializer):
	sessionid=serializers.CharField(max_length=999)
	class Meta:
		model=User
		fields=(
				'username',
				'email',
				'password',
				'sessionid'
			)
		read_only_fields=(
				'last_login',
				'staff_status',
				'active',
				'date_joined',
				'groups',
				'user_permissions'
			)

class LoginUserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=(
				'username',
				'password',
			)