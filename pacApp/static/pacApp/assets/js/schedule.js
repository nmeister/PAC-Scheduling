function openDay(tab, id) {
	// console.log(tab);
	// console.log(id);
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
  // console.log('#' + id);
  // console.log($('#' + id).data('date'));
  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tab).style.display = "block";
  document.getElementById(id).className += " active";
  // $(id).addClass(" active");
  // evt.currentTarget.className += " active";
}


function book(id) {
	// console.log('booking')
	let col = id;
	// console.log(col);
	var studioNum= col.match(/[a-z]+|[^a-z]+/gi);
	// console.log(studioNum[0])
	// console.log(studioNum[1]);
	var studio = studioNum[0]
	var day = studioNum[1] % 10; 
	var hour = studioNum[1] / 10;
	// console.log(day);
	// console.log(Math.trunc(hour));
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

// upon clicking on the BOOK button will make a future booking 
/* function futurebooks() {
	console.log('future booking');
	var futureinput = document.getElementById("future");
	var modal = document.getElementById("myModal");
	var regConfirm = document.getElementById("confirm");
	var futureConfirm = document.getElementById("futureConfirm");

	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];
	modal.style.display = "block";
	regConfirm.style.display = "none";
	futureinput.style.display = "block";
	futureConfirm.style.display = "block";

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	  futureinput.style.display = "none";
	  futureConfirm.style.display = "none";
	  regConfirm.style.display = "block";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	    futureinput.style.display = "none";
	    futureConfirm.style.display = "none";
	    regConfirm.style.display = "block";
	  }
	}
} */ 

// date is built as yyyy-mm-dd
function buildDate(date) {
	// console.log(date);
	let day = date.getDate();
	// JANUARY = 0 , FEB = 2
    let month = date.getMonth() + 1;
    // console.log(month)
    if (month < 10) {
      	month = '0' + String(month); 
     }
    let year = date.getFullYear(); 
    return year + '-' + month + '-' + day; 
}


function booking(studio,day,hour,id) {
	console.log('hello @ booking');
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
	// console.log($('#d'+day).data('date'));
	var date = $('#d'+day).data('date');
	/* var date = new Date();
	// console.log(date);
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
	bookdate.innerHTML = "Booked Day: " + date.toDateString(); */ 
	var bookdate = document.getElementById('bookdate');
	bookdate.innerHTML = "Booked Day: " + date.toDateString();

	var confirm = document.getElementById("confirm");
	// should have studio[start_time][dayofweek].yyyy-mm-dd
	confirm.value = id;
	confirm.value += '.';
	// dilliondance203.2020-04-15
	confirm.value += buildDate(date);
	
	
}

 function handleResponse(day) {  // get the response and show that in inner html 
 	console.log('before parse');
 	// var data = parse();
    // schedule(data);
 	// document.getElementById("scheduleOnHome").load();
 	console.log('success after booking');
 	// console.log(day);
 	
 	// console.log(id)
 	let id = "d" + day;
 	var days = ['sun','mon','tue','wed','thu','fri','sat'];
 	openDay(days[day],id);
 	
 }

function sendbook(id) {
	var modal = document.getElementById("myModal");
	modal.style.display = "none";
	var info = id.split('.');
	let url = 'create_booking';
	// parse the studio and the after numbers
	var studioNum = info[0].match(/[a-z]+|[^a-z]+/gi); 
	// what day is the booking occuring on 
	var day = Math.trunc(studioNum[1] % 10); 
	// start time of booking
	var hour = Math.trunc(studioNum[1] / 10);
	// gets name of the person who wants to book it 
	var name = document.getElementById('username').value;
	var date = info[1];
	// var date = info[1].replace('-', '/');
	// date = date.replace('-', '/');
	// console.log(date);
	// request made to create booking 
	request = $.ajax(
               {
                  type: "GET",
                  url: url,
                  data: {'studio': studioNum[0], // studio name 
                  		'date': date, // in the form of yyyy/mm/dd
                  		'starttime': hour, // int start time 
                  		'endtime': hour+1, 
                  		'day': day, // day of the week 
                  		'name': name, // name of person who is booking 
              		},
                  success: handleResponse(day),
               }
            );
	
}