from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields=(
			'first_name',
			'last_name',
			'email',
			'username',
			'password1',
			'password2',
		)
		labels={
			'first_name' : 'Nama Depan',
			'last_name' : 'Nama Belakang',
		}

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude=(
				'user',
				'status',
				'username',
				'koin',
				'user_level'
			)