from django.contrib import admin
from .models import VideoCourse,Course, VideoCourse, VideoComment, CourseStatus
# Register your models here.

admin.site.register(VideoCourse)
admin.site.register(Course)
admin.site.register(VideoComment)
admin.site.register(CourseStatus)