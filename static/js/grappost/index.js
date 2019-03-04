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

const divbaru = document.createElement('div');
divbaru.classList.add('container');
const inputgroup = document.createElement('div');
inputgroup.classList.add('input-group');
const formbaru = document.createElement('input');
formbaru.classList.add('form-group','form-control')
formbaru.setAttribute('placeholder','Komentar')
formbaru.setAttribute('name','comment')
formbaru.setAttribute('id','id_comment')
const inputgroupappend = document.createElement('div');
inputgroupappend.classList.add('input-group-append')
const tombol = document.createElement('button');
tombol.classList.add('btn','btn-primary')
const textTombol = document.createTextNode('Kirim');
tombol.appendChild(textTombol)
const linkbaru = document.createElement('a')
linkbaru.setAttribute('href','{% url "grappost:comment" post.id %}')
linkbaru.appendChild(tombol)
inputgroupappend.appendChild(linkbaru)
inputgroup.appendChild(formbaru)
inputgroup.appendChild(inputgroupappend)
divbaru.appendChild(inputgroup)

const postingan = document.querySelectorAll('div.index div.postingan')

const komentar = document.querySelectorAll('div.index div.postingan div.status img.komentar');

// komentar.forEach(function(kom){
// 	kom.addEventListener('click',function(e){
// 		e.target.parentElement.parentElement.parentElement.appendChild(divbaru)
// 	})
// })

komentar.forEach(function(kom){
	kom.addEventListener('click',function(e){
		e.target.parentElement.parentElement.parentElement.innerHTML = `
			<div class="container komentarbox">
				<form>
					<input type="text" class="form-group form-control">
					<button class="btn btn-primary">Post</button>
				</form>
			</div>
		`
	})
})