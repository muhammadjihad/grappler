const status = document.querySelector('div.userprofile div.boxlevel');
const textStatus = document.querySelector('div.userprofile div.boxlevel small');

if(textStatus.innerHTML.toLowerCase() == 'legend'){
	status.style.backgroundColor = 'purple';
}
if(textStatus.innerHTML.toLowerCase() == 'expert'){
	status.style.backgroundColor = 'red';
}
if(textStatus.innerHTML.toLowerCase() == 'master'){
	status.style.backgroundColor = 'black';
}
if(textStatus.innerHTML.toLowerCase() == 'competent'){
	status.style.backgroundColor = 'orange';
}
if(textStatus.innerHTML.toLowerCase() == 'beginner'){
	status.style.backgroundColor = 'blue';
}
if(textStatus.innerHTML.toLowerCase() == 'novice'){
	status.style.backgroundColor = 'lightgreen';
}

const harga = document.querySelector('.harga')
harga.addEventListener('click',function(e){
	e.target.style.boxShadow = '0 0 0 transparent'
})