const status = document.querySelectorAll('small.level');
status.forEach(function(el) {
	if(el.innerHTML.toLowerCase() == 'legend'){
		el.parentElement.classList.add('legend');
	}
	if(el.innerHTML.toLowerCase() == 'novice'){
		el.parentElement.classList.add('novice');
	}
	if(el.innerHTML.toLowerCase() == 'expert'){
		el.parentElement.classList.add('expert');
	}
	if(el.innerHTML.toLowerCase() == 'beginner'){
		el.parentElement.classList.add('beginner');
	}
	if(el.innerHTML.toLowerCase() == 'competent'){
		el.parentElement.classList.add('competent');
	}
	if(el.innerHTML.toLowerCase() == 'master'){
		el.parentElement.classList.add('master');
	}
});