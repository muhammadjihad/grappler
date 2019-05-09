from rest_framework import generics
from .serializers import(
	ListCourseSerializer,
	PostDetailSerializer,
	DetailCourseSerializer,
	UpdateCourseSerializer
)
from rest_framework import permissions
from graplearn.models import Course,CourseStatus
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

class CreateCourseAPIView(generics.CreateAPIView):
	queryset=Course.objects.all()
	serializer_class=PostDetailSerializer
	permission_classes=[permissions.IsAuthenticated]

	def perform_create(self, serializer):
		new_course=serializer.save(user=self.request.user)
		new_course=Course.objects.get(id=new_course.id)
		CourseStatus.objects.create(course=new_course)