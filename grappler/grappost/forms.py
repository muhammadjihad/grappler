from django import forms
from .models import Postingan,Komentar

class PostinganForm(forms.ModelForm):
	class Meta:
		model = Postingan
		fields = (
				'judul',
				'isi',
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