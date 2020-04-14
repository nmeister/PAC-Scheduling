function book(id) {
	console.log('booking')
	let col = id;
	console.log(col);
	var studioNum= col.match(/[a-z]+|[^a-z]+/gi);
	console.log(studioNum[0])
	console.log(studioNum[1]);
	var studio = studioNum[0]
	var day = studioNum[1] % 10; 
	var hour = studioNum[1] / 10;
	console.log(day);
	console.log(Math.trunc(hour));
	booking(studio,day,hour);
}

function getDayWeek(day) {

	var days = ['Sunday','Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	return days[day]
}

function findStudioName(studio) {
	var studioList = {'wilcox':'Wilcox',
	'bloomberg':'Bloomberg', 
	'dilliondance':'Dillion Dance',
	'dillionmpr': 'Dillion MPR',
	'roberts':'Roberts LCA',
	'murphy':'Murphy LCA',
	'ns': 'New South',
	'forbes': 'Forbes Dance',
	'ellie': 'Ellie LCA'
	}
	return studioList[studio]
}

function booking(studio,day,hour) {
	console.log('hello')
	var modal = document.getElementById("myModal");

	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];
	modal.style.display = "block";
	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
	}
	nameStudio = findStudioName(studio)
	var bookstudio = document.getElementById("bookstudio");
	bookstudio.innerHTML = 'Studio: ' + nameStudio;
	var bookstarttime = document.getElementById("bookstarttime");
	zone1 = 'AM';
	zone2 = 'AM';
	if (hour > 12) {
		zone1 = 'PM';
		zone2 = 'PM'
	}
	var starttime = Math.trunc(hour % 12); 
	var endtime = Math.trunc(hour % 12) + 1; 
	if (starttime == 0) {
		starttime = 12; 
		zone1 = 'AM';
		zone2 = 'AM';
	}
	if (endtime == 0) {
		endtime = 12;
		zone2 = 'AM';
	}
	bookstarttime.innerHTML = 'Time: ' + starttime + zone1 
	+ '-' + endtime + zone2;
	// var dayofweek = document.getElementById('dayofweek');
	// dayofweek.innerHTML = getDayWeek(day);
	var date = new Date();
	console.log(date);
	if (day >= date.getDay()) {
		currdate = date.getDate()
		date.setDate(currdate + (day - date.getDay()))
		console.log(date)
	}
	else {
		currdate = date.getDate()
		date.setDate(currdate + (7 - date.getDay()) + day)
		console.log(date)
	}
	var bookdate = document.getElementById('bookdate');
	bookdate.innerHTML = "Booked Day: " + date.toDateString();

}