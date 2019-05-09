from .serializers import CreateUserSerializer, LoginUserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth import authenticate,login, get_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import(
		SessionAuthentication,
		BasicAuthentication,
	)
from django.contrib.sessions.models import Session

def getUser(sessionkey):
	session=Session.objects.get(session_key=sessionkey)
	uid=session.get_decoded().get('_auth_user_id')
	return User.objects.get(id=uid)

class CreateUserAPIView(generics.CreateAPIView):
	query=User.objects.all()
	serializer_class=CreateUserSerializer
	permission_classes=[permissions.AllowAny]

	def perform_create(self,serializer):
		print(serializer.data)
		session_key=serializer.data['sessionid']
		print(get_user(self.request))
		# new_user_input=serializer.save()
		# new_user=User.objects.get(id=new_user_input.id)
		# new_user.set_password(new_user_input.password)
		# new_user.is_active=False
		# new_user.save()

class LoginUserAPIView(APIView):
	query=User.objects.all()
	serializer_class=LoginUserSerializer
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes=[permissions.AllowAny]

	def get(self,request,*args,**kwargs):
		content={
			'login_page':'welcome to login page',
			'body':'hellow world'
		}
		return Response(content)

	def post(self,request,*args,**kwargs):
		content={
			'Success':'You are login now'
		}
		username=request.data['username']
		password=request.data['password']
		user=authenticate(
				self.request,
				username=username,
				password=password,
			)
		if user:
			login(self.request,user)
			content={
				'Success':'You are login now',
				'sessionid':self.request.session.session_key
			}
			print(self.request.session)
			print("You're Login now using {}".format(username))
		else:
			content={
				'failed':'wrong credetials'
			}
			print("error")
		return Response(content)


class LogoutUserAPIView(APIView):

	def post(self,request,*args,**kwargs):
		content={
			"pesan":"Terimakasih telah menggunakan Flixnote",
			"data":request.data
		}
		print(getUser(request.data['sessionid']))
		Session.objects.get(session_key=request.data["sessionid"]).delete()
		return Response(content)