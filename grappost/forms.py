from django import forms
from .models import Postingan,Komentar

class PostinganForm(forms.ModelForm):
	class Meta:
		model = Postingan
		fields = (
				'judul',
				'isi',
				'kategori_post',
				'file',
			)
		widgets = {
			'judul' : forms.TextInput(
					attrs = {
						'placeholder' : 'Apa yang mau kamu bagikan?',
						'class' : 'form-group form-control',
						'name' : 'judul'
					}
				),
			'isi' : forms.Textarea(
					attrs = {
						'placeholder' : 'Apa yang ingin kamu ceritakan?',
						'class' : 'form-group form-control',
					}
				)

		}

class KomentarForm(forms.ModelForm):
	class Meta:
		model = Komentar
		fields = ('isi',)
		widgets={
			'isi' : forms.Textarea(
				attrs={
					'placeholder' : 'Masukkan komentar di sini',
					'class' : 'form-group form-control',
				}
			)
		}