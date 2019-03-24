from rest_framework import generics
from .serializers import ListCourseSerializer, DetailCourseSerializer, UpdateCourseSerializer
from graplearn.models import Course
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import CourseLimitOffsetPagination, CoursePageNumberPagination

class ListCourseAPIView(generics.ListAPIView):
	queryset = Course.getAllCourse()
	serializer_class = ListCourseSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ('judul','kategori','user__username')
	pagination_class = CourseLimitOffsetPagination

class DetailCourseAPIView(generics.RetrieveAPIView):
	queryset = Course.objects.all()
	serializer_class = DetailCourseSerializer

class UpdateCourseAPIView(generics.RetrieveUpdateAPIView):
	queryset = Course.objects.all()
	serializer_class = UpdateCourseSerializer
	permission_classes = [IsOwnerOrReadOnly]
