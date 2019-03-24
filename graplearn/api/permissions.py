from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
	message="Kamu harus pemilik dari konten ini"
	def has_object_permission(self,request,view,obj):
		return obj.user == request.user