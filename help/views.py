from django.shortcuts import render

# Create your views here.

def index(request):
	context={
		'judul' : 'Bantuan'
	}
	return render(request,'help/index.html', context)
def koin(request):
	context={
		'judul' : 'Bantuan - Cara Mengisi Koin'
	}
	return render(request,'help/koin.html',context)
def tukarkoin(request):
	context={
		'judul' : 'Bantuan - Cara Menukar Koin'
	}
	return render(request,'help/tukarkoin.html',context)
def sistemlevel(request):
	context={
		'judul' : 'Bantuan - Sistem Leveling Flixnote'
	}
	return render(request,'help/sistemlevel.html',context)
def iklankursus(request):
	context={
		'judul' : 'Petunjuk - Cara Mengiklankan Kursus'
	}
	return render(request,'help/iklankursus.html',context)
def paketiklan(request):
	context={
		'judul' : 'Petunjuk - Paket iklan'
	}
	return render(request,'help/paketiklan.html',context)