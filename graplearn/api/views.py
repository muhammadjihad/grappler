from rest_framework import generics
from .serializers import ListCourseSerializer
from graplearn.models import Course
class ListCourseAPIView(generics.ListAPIView):
	queryset = Course.getAllCourse()
	serializer_class = ListCourseSerializer