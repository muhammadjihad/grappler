from django.shortcuts import render, redirect
from akun.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PostinganForm
from .models import Postingan, Komentar
# Create your views here.

@login_required
def index(request):

	current_user = User.objects.get(id = request.user.id)
	current_userPost = Postingan.objects.filter(user = current_user)
	current_userLike = []
	for post in current_userPost:
		for like in post.like.all():
			current_userLike.append(like)
	current_userComment = Komentar.objects.filter(user = current_user)
	profile = Profile.objects.get(user = current_user)
	allPost = Postingan.objects.all()
	allPost = allPost[::-1]
	likeCounter = []
	postLikeCounter = []
	for post in allPost:
		likeCounter.append((len(post.like.all()),post.id))
	likeCounter = sorted(likeCounter, reverse=True)
	trendingPostByLike = []
	for post in likeCounter:
		trendingPostByLike.append(Postingan.objects.get(id=post[1]))
	trendingPostByLike = trendingPostByLike[:2]

	context = {
		'judul' : 'Grappost | For Your Sharing',
		'jumboTag' : 'Ayo Sharing Ilmu Kamu!',
		'profile' : profile,
		'allPost' : allPost,
		'trendingPostByLike' : trendingPostByLike,
		'current_userPost' : current_userPost,
		'current_userLike' : len(current_userLike),
		'current_userComment' : len(current_userComment)
	}

	return render(request,'grappost/index.html', context)

def createpost(request):

	postinganForm = PostinganForm(request.POST or None,request.FILES or None)

	context = {
		'judul' : 'Mau berbagi apa hari ini?',
		'jumboTag' : 'Mau berbagi apa hari ini?',
		'postForm' : postinganForm

	}

	if request.method == 'POST':
		postinganForm = PostinganForm(request.POST,request.FILES)
		if postinganForm.is_valid():
			Postingan.objects.create(
					user = request.user,
					judul = postinganForm.cleaned_data.get('judul'),
					isi = postinganForm.cleaned_data.get('isi'),
					file = request.FILES['file']
				)
			return redirect('grappost:index')

	return render(request,'grappost/createpost.html', context)

def like(request,id_like):

	post = Postingan.objects.get(id = id_like)
	userLiked = post.like.all()
	if not request.user in userLiked:
		post.like.add(request.user)
		post.save()
	else:
		return redirect('grappost:index')

	return redirect('grappost:index')

def comment(request,id_comment):

	 post = Postingan.objects.get(id=id_comment)
	 isi = request.POST.get('comment')
	 Komentar.objects.create(
	 		postingan = post,
	 		isi = isi,
	 	)

	 return redirect('grappost:index')