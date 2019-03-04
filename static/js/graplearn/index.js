const status = document.querySelectorAll('.boxlevel small');
status.forEach(function(stat){
	if(stat.innerHTML.toLowerCase() == 'legend'){
		stat.parentElement.classList.add('legend');
	}
	if(stat.innerHTML.toLowerCase() == 'novice'){
		stat.parentElement.classList.add('novice');
	}
	if(stat.innerHTML.toLowerCase() == 'expert'){
		stat.parentElement.classList.add('expert');
	}
	if(stat.innerHTML.toLowerCase() == 'beginner'){
		stat.parentElement.classList.add('beginner');
	}
	if(stat.innerHTML.toLowerCase() == 'competent'){
		stat.parentElement.classList.add('competent');
	}
	if(stat.innerHTML.toLowerCase() == 'master'){
		stat.parentElement.classList.add('master');
	}
});