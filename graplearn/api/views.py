from rest_framework import generics
from .serializers import ListCourseSerializer, DetailCourseSerializer, UpdateCourseSerializer
from graplearn.models import Course
from .permissions import IsOwnerOrReadOnly
class ListCourseAPIView(generics.ListAPIView):
	queryset = Course.getAllCourse()
	serializer_class = ListCourseSerializer

class DetailCourseAPIView(generics.RetrieveAPIView):
	queryset = Course.objects.all()
	serializer_class = DetailCourseSerializer

class UpdateCourseAPIView(generics.RetrieveUpdateAPIView):
	queryset = Course.objects.all()
	serializer_class = UpdateCourseSerializer
	permission_classes = [IsOwnerOrReadOnly]
