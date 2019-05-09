from django.shortcuts import render
from graplearn.models import Course, CourseStatus
from operator import itemgetter

def index(request):

	userCourses = Course.objects.all()
	userLike = []
	for course in userCourses:
		userLike.append((
			(CourseStatus.objects.get(course=course).like.all().count()*0.3)+(CourseStatus.objects.get(course=course).student.all().count()*0.7)
			,course.id))
	sortedCourse = (sorted(userLike, reverse=True))
	trendingCourses = []
	i = 0
	while i<len(sortedCourse):
		trendingCourses.append(Course.objects.get(id=sortedCourse[i][1]))
		i += 1
	showCourses = trendingCourses[:6]

	context = {
		'judul' : 'Flixnote | The Most Online Learning in Indonesia',
		'jumboTag' : 'Learn Anything, Get Everything',
		'trendingCourses' : showCourses
	}

	return render(request,'index.html',context)