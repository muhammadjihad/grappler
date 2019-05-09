const status = document.querySelector('div.container div.profilecontainer p');
console.log(status)
if(status.innerHTML.toLowerCase() == 'legend'){
	status.parentElement.classList.add('legend');
}
if(status.innerHTML.toLowerCase() == 'novice'){
	status.parentElement.classList.add('novice');
}
if(status.innerHTML.toLowerCase() == 'expert'){
	status.parentElement.classList.add('expert');
}
if(status.innerHTML.toLowerCase() == 'beginner'){
	status.parentElement.classList.add('beginner');
}
if(status.innerHTML.toLowerCase() == 'competent'){
	status.parentElement.classList.add('competent');
}
if(status.innerHTML.toLowerCase() == 'master'){
	status.parentElement.classList.add('master');
}

const kategori_post = document.querySelectorAll('span.kategoripost')
console.log(kategori_post)
kategori_post.forEach(function(kategori){
	if(kategori.innerHTML == 'Mencari'){
		kategori.className += ' mencari'
	} else if (kategori.innerHTML == 'Promo'){
		kategori.className += ' promo'
	} else if (kategori.innerHTML == 'Bertanya'){
		kategori.className += ' bertanya'
	}
});