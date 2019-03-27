from django.contrib import admin
from .models import Profile, Friend, Proyek, Dompet, MyCourse, OpeningVideo, Testimoni
# Register your models here.

admin.site.register(Friend)
admin.site.register(Profile)
admin.site.register(Proyek)
admin.site.register(Dompet)
admin.site.register(MyCourse)
admin.site.register(OpeningVideo)
admin.site.register(Testimoni)