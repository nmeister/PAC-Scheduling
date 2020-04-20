/* this gets called when we click on one of the tabs */ 
function openDay(tab, id) {

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
  document.getElementById(id).className += " active";

}

/* when we click on one of the empty cells, checks to see if we are on a page that allows
	us to book, if yes we call book function, else we print to console and return */ 
function canEdit(id) {
	var editable = $('#schedule').data('editable');
	console.log(editable);
	if (editable == 'True') {
		book(id);
	}
	else {
		console.log('Not allowed to book on this page. Please login to book')
		return;
	}
}

/* essentially just parses the information from the id and then passes it to booking */ 
function book(id) {

	var editable = $('#schedule').data('editable');


	let col = id;

	var studioNum= col.match(/[a-z]+|[^a-z]+/gi);

	var studio = studioNum[0]
	var day = studioNum[1] % 10; 
	var hour = studioNum[1] / 10;

	booking(studio,day,hour,id);
}

/* matches days of the week to the string */ 
function getDayWeek(day) {
	var days = ['Sunday','Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	return days[day];
}

/* corresponds studios identifier to the well formatted version */ 
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


// date is built as yyyy-mm-dd
// takes in a date object as input, outputs formatted string 
function buildDate(date) {
	// gets the dd 
	let day = date.getDate();
	// JANUARY = 0 , FEB = 2
	// gets the mm 
    let month = date.getMonth() + 1;
   
    if (month < 10) {
      	month = '0' + String(month); 
     }
    // gets the yyyy 
    let year = date.getFullYear(); 
    return year + '-' + month + '-' + day; 
}


// for getting the week number of a given date 
Date.prototype.getWeekNumber = function() { 
  var oneJan = new Date(this.getFullYear(), 0, 1); 
  
 // calculating number of days  
 //in given year before given date 
  
  var numberOfDays = Math.floor((this - oneJan) / (24 * 60 * 60 * 1000)); 
  // adding 1 since this.getDay() 
  //returns value starting from 0 
  
  return Math.ceil((this.getDay() + 1 + numberOfDays) / 7); 
} 

// gets called by book which passes in parsed version of the id 
/* this opens up the modal for the confirmed date to be booked */ 
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

	// corresponds the studio identitifer to the actual studio name 
	// updates html 
	nameStudio = findStudioName(studio);
	var bookstudio = document.getElementById("bookstudio");
	bookstudio.innerHTML = 'Studio: ' + nameStudio;
	// writing in the time of the booking 
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
	
	// writing in the date 
	var content = '#content' + day;
	console.log($(content).data('date'));
	var dateArr = $(content).data('date').split('-');
	var date = new Date(dateArr[0], dateArr[1]-1, dateArr[2]);

	var bookdate = document.getElementById('bookdate');
	// console.log(date)
	bookdate.innerHTML = "Booking Day: " + date.toDateString();

	var confirm = document.getElementById("confirm");
	// should have studio[start_time][dayofweek].yyyy-mm-dd
	confirm.value = id;
	confirm.value += '.';
	// dilliondance203.2020-04-15 (this is what confirm.value should look like)
	confirm.value += buildDate(date);
	console.log(confirm.value)
}

/* this response handles after callback from changing the week, updates data */ 
function handleresponse(response) 
{
    $('#schedule').html(response);
    showConfirm(); 

}

/* makes updates to the schedule via ajax call by url /update?=newdate= */ 
function setupWeek()
	
	{	
        console.log('in setupweek');
        // value of whatever is in the date input 
		var curr = $('#curr').val();
        let url = 'update';
        request = $.ajax(
               {
                  type: "GET",
                  url: url,
                  data: {'newdate': curr},
                  success: handleresponse,
               }
            );
    }

// sends this actual booking to backend to create a booking 
function sendbook(id) {
        var modal = document.getElementById("myModal");
        modal.style.display = "none";
        var info = id.split('.');
        
        // parse the studio and the after numbers
        var studioNum = info[0].match(/[a-z]+|[^a-z]+/gi); 
        // what day is the booking occuring on 
        var day = Math.trunc(studioNum[1] % 10); 
        // start time of booking
        var hour = Math.trunc(studioNum[1] / 10);
        // gets name of the person who wants to book it 
        var name = document.getElementById('username').value;
        var date = info[1];
        console.log($('#curr').val());
        var currweek = $('#curr').val()

        // request made for booking which updates schedule
        let url = 'update';
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
                          'newdate': currweek, 
                      },
                      success: handleresponse,
                   }
                );
     }


function showConfirm() {
	console.log('has been booked!');

}