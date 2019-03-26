const status = document.querySelector('div.profilecontainer small.level');
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