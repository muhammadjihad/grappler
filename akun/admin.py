from django.contrib import admin
from .models import Profile, Pesan , Friend, Proyek, Dompet, MyCourse, OpeningVideo, Testimoni, Complaining, TukarKoin, ExpiredCourse, Karya
# Register your models here.
class PublishedView(admin.ModelAdmin):
	readonly_fields=['waktu_dilakukan',]
class ExpiredStartDate(admin.ModelAdmin):
	readonly_fields=['start_date',]


admin.site.register(Friend)
admin.site.register(Profile)
admin.site.register(Proyek)
admin.site.register(Dompet)
admin.site.register(MyCourse)
admin.site.register(OpeningVideo)
admin.site.register(Testimoni)
admin.site.register(Complaining)
admin.site.register(TukarKoin, PublishedView)
admin.site.register(ExpiredCourse)
admin.site.register(Karya)
admin.site.register(Pesan)