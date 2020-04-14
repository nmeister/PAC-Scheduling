function openDay(evt, tab) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tab).style.display = "block";
  evt.currentTarget.className += " active";
}



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
	booking(studio,day,hour,id);
}

function getDayWeek(day) {

	var days = ['Sunday','Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	return days[day];
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
	};
	return studioList[studio];
}


function booking(studio,day,hour,id) {
	console.log('hello');
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
	nameStudio = findStudioName(studio);
	var bookstudio = document.getElementById("bookstudio");
	bookstudio.innerHTML = 'Studio: ' + nameStudio;
	var bookstarttime = document.getElementById("bookstarttime");
	zoneStart = 'AM';
	zoneEnd = 'AM';
	if (hour > 12) {
		zoneStart = 'PM';
		if (hour < 23) {
			zoneEnd = 'PM';
		}
	}
	var starttime = Math.trunc(hour % 12); 
	var endtime = Math.trunc(hour % 12) + 1; 
	if (starttime == 0) {
		starttime = 12; 
		zoneStart = 'AM';
		zoneEnd = 'AM';
	}
	if (endtime == 0) {
		endtime = 12;
		zoneEnd = 'AM';
	}
	bookstarttime.innerHTML = 'Time: ' + starttime + zoneStart + '-' + endtime + zoneEnd;
	// var dayofweek = document.getElementById('dayofweek');
	// dayofweek.innerHTML = getDayWeek(day);
	var date = new Date();
	console.log(date);
	if (day >= date.getDay()) {
		currdate = date.getDate();
		date.setDate(currdate + (day - date.getDay()));
		console.log(date);
	}
	else {
		currdate = date.getDate();
		date.setDate(currdate + (7 - date.getDay()) + day);
		console.log(date);
	}
	var bookdate = document.getElementById('bookdate');
	bookdate.innerHTML = "Booked Day: " + date.toDateString();


	var confirm = document.getElementById("confirm");
	confirm.value = id;
	confirm.value += '.';
	confirm.value += date.toDateString();
}

 function handleResponse(day) {  // get the response and show that in inner html 
 	window.location.reload();
 	console.log('success');
 	console.log(day);
 	let id = "d" + day;
 	console.log(id)
 	let curr = document.getElementById(id);
 	curr.click();


 }

function sendbook(id) {
	var modal = document.getElementById("myModal");
	modal.style.display = "none";
	var info = id.split('.');
	let url = 'create_booking';
	var studioNum = info[0].match(/[a-z]+|[^a-z]+/gi); 
	var day = Math.trunc(studioNum[1] % 10); 
	var hour = Math.trunc(studioNum[1] / 10);
	var name = document.getElementById('username').value;
	request = $.ajax(
               {
                  type: "GET",
                  url: url,
                  data: {'studio': studioNum[0],
                  		'date': info[1],
                  		'starttime': hour,
                  		'endtime': hour+1, 
                  		'day': day,
                  		'name':name,
              		},
                  success: handleResponse(day),
               }
            );
	
}