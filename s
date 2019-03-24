[1mdiff --git a/graplearn/api/serializers.py b/graplearn/api/serializers.py[m
[1mindex f067602..11a20c5 100644[m
[1m--- a/graplearn/api/serializers.py[m
[1m+++ b/graplearn/api/serializers.py[m
[36m@@ -25,8 +25,11 @@[m [mclass ListCourseSerializer(serializers.ModelSerializer):[m
 		}[m
 		return user[m
 [m
[32m+[m
[32m+[m
 class DetailCourseSerializer(serializers.ModelSerializer):[m
 	user = UserSerializer()[m
[32m+[m	[32mcourse_status = serializers.SerializerMethodField()[m
 	class Meta:[m
 		model = Course[m
 		fields=([m
[36m@@ -36,9 +39,18 @@[m [mclass DetailCourseSerializer(serializers.ModelSerializer):[m
 				'deskripsi',[m
 				'harga',[m
 				'published',[m
[31m-				'like',[m
[31m-				'view',[m
[32m+[m				[32m'course_status'[m
 			)[m
[32m+[m	[32mdef get_course_status(self,obj):[m
[32m+[m		[32mcourse_status = obj.coursestatus[m
[32m+[m		[32mcourse_status = course_status.like.all()[m
[32m+[m		[32muserlike = [][m
[32m+[m		[32mfor user in course_status:[m
[32m+[m			[32muserlike.append(user.username)[m
[32m+[m		[32mdata = {[m
[32m+[m			[32m"user_like" : userlike[m
[32m+[m		[32m}[m
[32m+[m		[32mreturn data[m
 [m
 class UpdateCourseSerializer(serializers.ModelSerializer):[m
 	class Meta:[m
[1mdiff --git a/graplearn/models.py b/graplearn/models.py[m
[1mindex 5651eb1..9cb6f93 100644[m
[1m--- a/graplearn/models.py[m
[1m+++ b/graplearn/models.py[m
[36m@@ -52,8 +52,8 @@[m [mclass Course(models.Model):[m
 [m
 class CourseStatus(models.Model):[m
 	course = models.OneToOneField(Course, on_delete=models.CASCADE)[m
[31m-	like = models.ManyToManyField(User, blank=True,null=True, related_name='like')[m
[31m-	view = models.ManyToManyField(User, blank=True,null=True, related_name='view')[m
[32m+[m	[32mlike = models.ManyToManyField(User, blank=True, related_name='like')[m
[32m+[m	[32mview = models.ManyToManyField(User, blank=True, related_name='view')[m
 [m
 	def __str__(self):[m
 		return self.course.judul[m
[1mdiff --git a/graplearn/views.py b/graplearn/views.py[m
[1mindex 3af9f3f..ed87d50 100644[m
[1m--- a/graplearn/views.py[m
[1m+++ b/graplearn/views.py[m
[36m@@ -47,6 +47,15 @@[m [mdef index(request):[m
 def index_filter(request,filter_input,judul_input):[m
 [m
 	ListCourse = None[m
[32m+[m	[32mcourse_status = [][m
[32m+[m
[32m+[m	[32mdef arrangement():[m
[32m+[m		[32mfor course in ListCourse:[m
[32m+[m			[32meach_course = CourseStatus.objects.get_or_create(course=course)[m
[32m+[m			[32muser_liked_course = each_course[0].like.all()[m
[32m+[m			[32mcourse_status.append([m
[32m+[m				[32m(user_liked_course,course)[m
[32m+[m				[32m)[m
 [m
 	if filter_input == "judul":[m
 		ListCourse = Course.objects.filter(judul__contains=judul_input)[m
[36m@@ -58,11 +67,12 @@[m [mdef index_filter(request,filter_input,judul_input):[m
 		ListCourse = Course.objects.all().order_by("-id")[m
 	else:[m
 		return redirect("graplearn:index")[m
[32m+[m	[32marrangement()[m
 [m
 	context = {[m
 		'judul' : 'graplearn | Learn Everything',[m
 		'jumboTag' : 'Pilih Kursus yang kamu suka!',[m
[31m-		'ListCourse' : ListCourse,[m
[32m+[m		[32m'ListCourse' : course_status,[m
 		'all' : 'all',[m
 	}[m
 [m
