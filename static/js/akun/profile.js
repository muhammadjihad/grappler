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

var openingVideo = document.querySelectorAll("video.openingvideo")
openingVideo.forEach(function(el){
	var this_playtoggle=el.nextElementSibling.children[0]
	var this_seekslider = el.nextElementSibling.children[1]
	var this_current_time_text = el.nextElementSibling.children[2]
	var this_duration_time_text = el.nextElementSibling.children[3]
	var this_volumeslider = el.nextElementSibling.children[4]
	var this_fullscreen = el.nextElementSibling.children[5]

	this_playtoggle.addEventListener('click',function(){
				if(el.paused){
					el.play()
					this_playtoggle.innerHTML='Pause'
					this_playtoggle.classList.remove("btn-primary")
					this_playtoggle.classList.add("btn-danger")
				} else {
					el.pause()
					this_playtoggle.innerHTML='Play '
					this_playtoggle.classList.remove("btn-danger")
					this_playtoggle.classList.add("btn-primary")
				}
			},false);
			
	this_seekslider.addEventListener('change',function(){
					var seekto = el.duration*(seekslider.value/100)
					el.currentTime=seekto
				},false);

	el.addEventListener('click',function(){
					if(el.paused){
						el.play()
						this_playtoggle.innerHTML='Pause'
						this_playtoggle.classList.remove("btn-primary")
						this_playtoggle.classList.add("btn-danger")
					} else {
						el.pause()
						this_playtoggle.innerHTML='Play'
						this_playtoggle.classList.remove("btn-danger")
						this_playtoggle.classList.add("btn-primary")
					}
			},false);
				
	el.addEventListener('timeupdate',function(){
					var new_time=el.currentTime*(100/el.duration)
					this_seekslider.value=new_time
					var curmins=Math.floor(el.currentTime/60)
					var cursecs=Math.floor(el.currentTime - curmins * 60)
					var durmins =Math.floor(el.duration/60)
					var dursecs =Math.floor(el.duration-durmins * 60)

					if(cursecs<10){
						cursecs="0" +cursecs
					}
					if(dursecs<10){
						dursecs="0"+dursecs
					}

					this_current_time_text.innerHTML=curmins+':'+cursecs
					this_duration_time_text.innerHTML=durmins+':'+dursecs
				},false);

	this_volumeslider.addEventListener('change',function(){
		el.volume=this_volumeslider.value/100
	},false);

	this_fullscreen.addEventListener('click',function(){
		if(el.requestFullscreen){
			el.requestFullscreen()
		} else if(el.webkitRequestFullScreen){
			el.webkitRequestFullScreen()
		} else if(el.mozRequestFullScreen){
			el.mozRequestFullScreen()
		}
	},false);

	el.addEventListener('dblclick',function(){
		if(el.requestFullscreen){
			el.requestFullscreen()
		} else if(el.webkitRequestFullScreen){
			el.webkitRequestFullScreen()
		} else if(el.mozRequestFullScreen){
			el.mozRequestFullScreen()
		}
	})

});