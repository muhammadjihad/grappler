from rest_framework import generics
from .serializers import ListCourseSerializer, DetailCourseSerializer
from graplearn.models import Course
class ListCourseAPIView(generics.ListAPIView):
	queryset = Course.getAllCourse()
	serializer_class = ListCourseSerializer

class DetailCourseAPIView(generics.RetrieveAPIView):
	queryset = Course.objects.all()
	serializer_class = DetailCourseSerializer