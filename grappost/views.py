from django.shortcuts import render, redirect, reverse
from akun.models import Profile, Friend
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PostinganForm, KomentarForm
from .models import Postingan, Komentar
from django.core.paginator import Paginator
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
	trendingPostByLike = trendingPostByLike[:5]
	current_user_friend, created = Friend.objects.get_or_create(current_user = request.user)
	current_user_friend = current_user_friend.users.all()
	allPost = Postingan.objects.filter(user__in=current_user_friend)
	allPost = Paginator(allPost,6)
	page = request.GET.get('page')
	allPost = allPost.get_page(page)


	context = {
		'judul' : 'Grappost | For Your Sharing',
		'jumboTag' : 'Ayo Sharing Ilmu Kamu!',
		'profile' : profile,
		'allPost' : allPost,
		'trendingPostByLike' : trendingPostByLike,
		'current_userPost' : current_userPost,
		'current_userLike' : len(current_userLike),
		'current_userComment' : len(current_userComment),
		'current_user_friend' : current_user_friend,
	}

	if len(current_user_friend) == 0:
		context['nofriend'] = 'nofriend'

	return render(request,'grappost/index.html', context)

@login_required
def index_all_filter(request, parameter, judul_post):

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
	trendingPostByLike = trendingPostByLike[:5]
	current_user_friend, created = Friend.objects.get_or_create(current_user = request.user)
	current_user_friend = current_user_friend.users.all()

	if parameter != 'all' and judul_post == 'none':
		allPost = Postingan.objects.filter(kategori_post=parameter).order_by("-id")
	elif parameter == 'all' and judul_post != 'none' and judul_post != 'all':
		allPost = Postingan.objects.filter(judul__contains = judul_post).order_by("-id")
	elif parameter != 'all' and judul_post != 'none' and judul_post != 'all':
		allPost = Postingan.objects.filter(kategori_post__iexact = parameter,judul__contains=judul_post).order_by("-id")

	allPost = Paginator(allPost,6)
	page = request.GET.get('page')
	allPost = allPost.get_page(page)

	context = {
		'judul' : 'Grappost | For Your Sharing',
		'jumboTag' : 'Ayo Sharing Ilmu Kamu!',
		'profile' : profile,
		'allPost' : allPost,
		'trendingPostByLike' : trendingPostByLike,
		'current_userPost' : current_userPost,
		'current_userLike' : len(current_userLike),
		'current_userComment' : len(current_userComment),
		'current_user_friend' : current_user_friend,
		'all' : 'all',
	}

	if len(current_user_friend) == 0:
		context['nofriend'] = 'nofriend'

	if request.method == "POST":
		parameter = request.POST['kategori']
		judul = request.POST.get('judul')
		if judul == '':
			judul = 'none'
		return redirect(reverse("grappost:index_all", kwargs={
				'parameter' : parameter,
				'judul_post' : judul,
			}))

	return render(request,'grappost/index.html', context)

@login_required
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
			new_post = postinganForm.save(commit=False)
			new_post.user = request.user
			new_post.save()
			userProfile = Profile.objects.get(user = request.user)
			userProfile.gainExp(10*int(userProfile.user_level))
			return redirect('grappost:index')

	return render(request,'grappost/createpost.html', context)

@login_required
def like(request,id_like):

	post = Postingan.objects.get(id = id_like)
	userLiked = post.like.all()
	if not request.user in userLiked:
		post.like.add(request.user)
		post.save()
		userProfile = post.user.profile
		userProfile.gainExp(10*int(userProfile.user_level))
	elif request.user in userLiked:
		post.like.remove(request.user)
		post.save()
		userProfile = post.user.profile
		userProfile.un_gainExp(10*int(userProfile.user_level))
	return redirect('grappost:index')

@login_required
def comment(request,id_comment):
	postingan = Postingan.objects.get(id=id_comment)
	komentarForm = KomentarForm
	komentar_postingan = Komentar.objects.filter(postingan = postingan)
	user_profile = Profile.objects.get(user = request.user)
	context={
		'judul':'Flixnote | Online Learning Marketplace',
		'postingan' : postingan,
		'komentarForm' : komentarForm,
		'komentar_postingan' : komentar_postingan,
	}

	if request.user == postingan.user:
		context['current_user'] = 'current_user'

	if request.method == 'POST':
		komentarForm = KomentarForm(request.POST)
		if komentarForm.is_valid():
			new_komentar = komentarForm.save(commit=False)
			new_komentar.postingan = postingan
			new_komentar.user = request.user
			new_komentar.save()
			return redirect(reverse("grappost:comment",kwargs={
			'id_comment' : postingan.id
			}))


	return render(request,'grappost/createcomment.html',context)

@login_required
def deletePost(request,id_post):
	postingan = Postingan.objects.get(id=id_post)
	profile_target = Profile.objects.get(user = postingan.user)
	if request.user == postingan.user:
		postingan.delete()
		profile_target.un_gainExp(10*int(profile_target.user_level))
	return redirect("akun:profile")

@login_required
def deleteKomen(request,id_komen):
	komentar = Komentar.objects.get(id=id_komen)
	profile_target = Profile.objects.get(user = komentar.user)
	if request.user == komentar.user:
		komentar.delete()
		if komentar.postingan.kategori_post == '3':
			profile_target.un_gainExp(35*int(user_profile.user_level))
		if komentar.postingan.kategori_post == '3':
			profile_target.un_gainExp(10*int(user_profile.user_level))
	return redirect(reverse("grappost:comment",kwargs={
			'id_comment' : komentar.postingan.id
		}))

@login_required
def help_comment(request,operation,id_comment):
	komentar = Komentar.objects.get(id=id_comment)
	if komentar.helping == True and operation == 'helping':
		return redirect("grappost:index_all")
	elif komentar.helping == False and operation == 'nothelping':
		return redirect("grappost:index_all")
	def comment_like_system(jenis_posting,sender_user,receiver_user):
		selisih = int(sender_user.user_level)-int(receiver_user.user_level)
		if jenis_posting.kategori_post == '3' and operation == 'helping':
			if selisih == 5:
				sender_user.gainExp(350*int(sender_user.user_level))
			elif selisih == 4:
				sender_user.gainExp(280*int(sender_user.user_level))
			elif selisih == 3:
				sender_user.gainExp(120*int(sender_user.user_level))
			elif selisih == 2:
				sender_user.gainExp(30*int(sender_user.user_level))
			elif selisih == 1:
				sender_user.gainExp(15*int(sender_user.user_level))
			else:
				sender_user.gainExp(5*int(sender_user.user_level))
			komentar.helping = True
			komentar.save()
		if jenis_posting.kategori_post == '3' and operation == 'nothelping':
			if selisih == 5:
				sender_user.un_gainExp(350*int(sender_user.user_level))
			elif selisih == 4:
				sender_user.un_gainExp(280*int(sender_user.user_level))
			elif selisih == 3:
				sender_user.un_gainExp(120*int(sender_user.user_level))
			elif selisih == 2:
				sender_user.un_gainExp(30*int(sender_user.user_level))
			elif selisih == 1:
				sender_user.un_gainExp(15*int(sender_user.user_level))
			else:
				sender_user.un_gainExp(5*int(sender_user.user_level))
			komentar.helping = False
			komentar.save()
		else:
			sender_user.gainExp(2*int(sender_user.user_level))		
	
	if request.user == komentar.postingan.user:
		comment_like_system(komentar.postingan,komentar.user.profile,komentar.postingan.user.profile)
		
	return redirect(reverse("grappost:comment",kwargs={
			'id_comment' : komentar.postingan.id
		}))
		
