from django import forms
from .models import Course, VideoCourse, VideoComment


class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = (
			'judul',
			'kategori',
			'deskripsi',
			'harga',
			'thumbnail',
		)
		widgets={
			'judul' : forms.TextInput(
					attrs = {
						'class' : 'form-group form-control',
						'placeholder' : 'Masukkan judul kursus',
					}
				),
			'kategori' : forms.TextInput(
					attrs = {
						'class' : 'form-group form-control',
						'placeholder' : 'Masukkan kategori',
					}
				),

			'deskripsi' : forms.Textarea(
					attrs = {
						'class' : 'form-group form-control',
						'placeholder' : 'Deskripsi Kursus',
					}
				),
			'harga' : forms.NumberInput(
					attrs = {
						'class' : 'form-control form-group',
						'placeholder' : "Harga Kursus"
					}
				),
			'thumbnail' : forms.FileInput(
				),
		}

class VideoCourseForm(forms.ModelForm):
	class Meta:
		model = VideoCourse
		fields=(
				'judul',
				'video',
				'deskripsi',
				'referensi',
			)

class VideoCommentForm(forms.ModelForm):
	class Meta:
		model = VideoComment
		fields = (
				'comment',
			)
		widgets = {
			'comment' : forms.Textarea(
					attrs = {
						'placeholder' : 'Komentar ...',
						'class' : 'form-group form-control'
					} 
				)

		}
		labels = {
			'comment' : ''

		}