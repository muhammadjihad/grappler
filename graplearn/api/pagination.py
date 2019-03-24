from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class CourseLimitOffsetPagination(LimitOffsetPagination):
	default_limit = 5
	max_limit = 10

class CoursePageNumberPagination(PageNumberPagination):
	page_size = 5