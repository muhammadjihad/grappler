from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, OpeningVideo, Testimoni, Proyek, Complaining, Karya, Pesan

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
				'user_level',
				'user_exp',
				'verified',
			)
		labels={
			'thumbnail' : 'banner',
			'whatsapp_account' : 'WhatsApp',
			'line_account' : 'Line',
		}

class OpeningVideoForm(forms.ModelForm):
	class Meta:
		model = OpeningVideo
		fields=(
				'judul',
				'video',
			)

class TestimoniForm(forms.ModelForm):
	class Meta:
		model = Testimoni
		fields=('testimoni',)
		widgets={
			'testimoni':forms.Textarea(
					attrs={
						'class':'form-group form-control',
						'placeholder':'masukkan testimoni atau kesan kamu terhadap user ini',
					}
				)
		}

class PenghargaanForm(forms.ModelForm):
	class Meta:
		model = Proyek
		exclude=('user','waktu',)

class ComplainingForm(forms.ModelForm):
	class Meta:
		model = Complaining
		fields=(
			'komplain',
			'saran',
		)
		widgets={
			'komplain' : forms.Textarea(
					attrs={
						'class':'form-control form-group',
						'placeholder' : 'Menurutmu apa yang masih kurang?',
						'rows':"5"
					}
				),
			'saran' : forms.Textarea(
					attrs={
						'class':'form-control form-group',
						'placeholder' : 'Menurutmu seharusnya seperti apa?',
						'rows':"5"
					}
				)
		}

class KaryaForm(forms.ModelForm):
	class Meta:
		model=Karya
		exclude=('user',)
		widgets={
			'judul':forms.TextInput(
					attrs={
						'placeholder':'Masukkan judul Karya yang kamu buat',
					}
				),
			'keterangan' : forms.Textarea(
					attrs={
						'placeholder' : 'Masukkan Keterangan Karya yang telah kamu buat',
						'rows' : "5"
					}
				)
		}

class PesanForm(forms.ModelForm):
	class Meta:
		model=Pesan
		fields=(
			'pesan',
			'file',
		)
		widgets={
			'pesan':forms.Textarea(
					attrs={
						'class':'form-group form-control',
						'placeholder':'Masukkan Pesan',
						'row':'3'
					}
				),
}