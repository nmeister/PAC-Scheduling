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
  for (i = 0; i < 7; i++) {
  	 $('#d'+i+'date').css('display','none');
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tab).style.display = "block";
  document.getElementById(id).className += " active";
  var weekdays= {'sun':0,'mon':1,'tue':2,'wed':3,'thu':4,'fri':5,'sat':6};
  var date = $('#'+id).data('date').split('-');
  console.log(date)
  var reformatted = date[1] + '/' + date[2] + '/' + date[0].substring(2,4); 
  console.log(date[0].substring(2));
  console.log(date[0].substring(2));
  $('#'+id+'date').html(reformatted);
  $('#'+id+'date').css('display','block');
}


function handleBad(msg) {
  $('#badmsg').html(msg);
  var modal = document.getElementById("handlebad");
  // $('#myModal').css('display','block');
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("closebad");
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
      // make sure they are unchecked when we close 
    }
  }
  var ok = document.getElementById("byebad");
  ok.onclick = function() {
    modal.style.display = "none";
  }
}

function cannotEdit() {
    console.log('cannot book');
}

function homeCannotBook() {
  console.log('home cannot book error');
  
  // handles all modal - make it seen 
  var modal = document.getElementById("errorHome");
 
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("errorHomeClose");
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

  // login button will show up and then if not already logged in
  // should should login in button otherwise booking 
  // need to fix once we have cas 
  var login = document.getElementById("okHome");
  login.onclick = function() {
    modal.style.display = "none";
    location.href = "schedule";
  }

}

// if we are within current hour and they still want to book 
function withinCurrentHourBooking(left, id) {
  console.log('within current hour booking');
  $('#minLeft').html(left);
  // handles all modal - make it seen 
  var modal = document.getElementById("currHour");
 
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("currClose");
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
     $("input[name='continue']:checked").prop('checked', false); 
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
       $("input[name='continue']:checked").prop('checked', false); 
      modal.style.display = "none";
    }
  }

  // should should login in button otherwise booking 
  // need to fix once we have cas 
  var input; 
  var currOK = document.getElementById("currOK");
  var yes = document.getElementById("yes");
  yes.onclick = function() {
    modal.style.display = "none";
    book(id);
  }
  var no = document.getElementById("no");
  no.onclick = function() {
     modal.style.display = "none";
     return;
  }

}

function canEdit(id) {
  console.log('id in canEdit' + id);
	var editable = $('#schedule').data('editable');
	console.log(editable);
  if (editable == 'False') {
      homeCannotBook(); 
      return;
  }
  var studioNum= id.match(/[a-z]+|[^a-z]+/gi);
  console.log(studioNum)
  var day = studioNum[1] % 10;
  var hour = studioNum[1] / 10;
  var content = '#content' + day;
  var dateArr = $(content).data('date').split('-');
  if (hour == 1) {
    dateArr[2] += 1; 
  }
  var strictdate = new Date(dateArr[0], dateArr[1]-1, dateArr[2], hour);
  var nextHour = new Date(dateArr[0], dateArr[1]-1, dateArr[2], hour+1);
  var today = new Date();
  console.log(today);
  console.log(strictdate);
  console.log('current right now' + today.getTime());
  console.log('this timeslot' + strictdate.getTime());

  var stillBook = 'no'
  if (strictdate.getTime() < today.getTime()) {
      if (today.getTime() - strictdate.getTime() < 55 * 60000) {
        console.log('still within 55 minutes');
        var minLeft = Math.trunc((nextHour.getTime() - today.getTime()) / 60000)
        var stillBook = withinCurrentHourBooking(minLeft, id);
        return;
      }
      editable = 'False'
  }
	if (editable == 'True') {

		book(id);
	}
	else {
		pastTime();
	}
}

function pastTime() {
  console.log('past the time error');
  
  // handles all modal - make it seen 
  var modal = document.getElementById("errorPast");
 
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("errorClose");
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

  // closing with oK button 
  var ok = document.getElementById("okbutton");
  ok.onclick = function() {
    modal.style.display = "none";
  }
}



function book(id) {
	// console.log('booking')
	var editable = $('#schedule').data('editable');
	console.log(editable);
	if (editable == 'False') {
		console.log('here')
		$('#' + id).on('click', '');
	}
	let col = id;
	// console.log(col);
	var studioNum= col.match(/[a-z]+|[^a-z]+/gi);
	// console.log(studioNum[0])
	// console.log(studioNum[1]);
	var studio = studioNum[0]
	var day = studioNum[1] % 10; 
	var hour = studioNum[1] / 10;
	console.log(day);
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
	'dillondance':'Dillon Dance',
	'dillonmar':'Dillon MAR',
	'dillonmpr': 'Dillon MPR',
	'murphy':'Murphy LCA',
	'ns': 'New South',
	'nswarmup': 'New South Warmup',
	'nstheatre': 'New South Theatre',
	'whitman': 'Whitman',
	'wilcox': 'Wilcox'
	};
	return studioList[studio];
}


// date is built as yyyy-mm-dd
function buildDate(date) {
	// console.log(date);
	let day = date.getDate();
  if (day < 10) {
     day = '0' + String(day); 
  }
	// JANUARY = 0 , FEB = 2
  let month = date.getMonth() + 1;
  // console.log(month)
  if (month < 10) {
    month = '0' + String(month); 
  }
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


function booking(studio,day,hour,id) {
	console.log('hello @ booking');
	
	// handles all modal - make it seen 
	var modal = document.getElementById("myModal");
	// $('#myModal').css('display','block');
	// Get the <span> element that closes the modal on the x button 
	var span = document.getElementsByClassName("close")[0];
	modal.style.display = "block";
	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
    $('#self').prop("checked", false);
    $('#group').prop("checked", false);
    $("#selfname").val('');
    $("input[name='usertype']:checked").prop('checked', false); 
    document.getElementById("selectgroup").selectedIndex = 0;
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
      // make sure they are unchecked when we close 
      $('#self').prop("checked", false);
      $('#group').prop("checked", false);
      $("#selfname").val('');
      $("input[name='usertype']:checked").prop('checked', false); 
      document.getElementById("selectgroup").selectedIndex = 0;
	  }
	}

	nameStudio = findStudioName(studio);
	var bookstudio = document.getElementById("bookstudio");
	bookstudio.innerHTML = 'Studio: ' + nameStudio;
	var bookstarttime = document.getElementById("bookstarttime");
	zoneStart = 'AM';
	zoneEnd = 'AM';
	if (hour >= 12) {
		zoneStart = 'PM';
		if (hour < 23) {
			zoneEnd = 'PM';
		}
	}
  if (Math.trunc(hour) == 11) {
    zoneEnd = 'PM';
  }
	var starttime = Math.trunc(hour % 12); 
  console.log(starttime);
  if (starttime == 0) {
    starttime = 12;
  }

	var endtime = Math.trunc(hour % 12) + 1; 
  console.log('hour ' + hour);
	if (Math.trunc(hour) > 23) {
		starttime = 12; 
		zoneStart = 'AM';
		zoneEnd = 'AM';
	}
	if (endtime == 0) {
		endtime = 12;
		zoneEnd = 'AM';
	}
	bookstarttime.innerHTML = 'Time: ' + starttime + zoneStart + '-' + endtime + zoneEnd;
	// vardayofweek = document.getElementById('dayofweek');
	// dayofweek.innerHTML = getDayWeek(day);
	
	
  
	var content = '#content' + day;
	console.log($(content).data('date'));
	var dateArr = $(content).data('date').split('-');
  console.log(dateArr);
  var date = new Date(dateArr[0], dateArr[1]-1, dateArr[2]);
  if (Math.trunc(hour) > 23) {
    var nextday = parseInt(dateArr[2]) + 1
    date = new Date(dateArr[0], dateArr[1]-1, nextday);
  }
  console.log(date);
	var bookdate = document.getElementById('bookdate');
	// console.log(date)
	bookdate.innerHTML = "Booking Day: " + date.toDateString();

	var confirm = document.getElementById("confirm");
	// should have studio[start_time][dayofweek].yyyy-mm-dd
	confirm.value = id;
	confirm.value += '.';
	// dilliondance203.2020-04-15
	confirm.value += buildDate(date);
	console.log(confirm.value)
}
// handles ajax response callback by changing the schedule 
function handleresponse(response) 
{
	console.log('handle after update');
  $('#schedule').html(response);
}

function handleBadDate() {

  var modal = document.getElementById("badDate");
  // $('#myModal').css('display','block');
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("closeBadDate");
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
      // make sure they are unchecked when we close 
    }
  }
  var ok = document.getElementById("okbadDate");
  ok.onclick = function() {
    modal.style.display = "none";
  }
  var today = buildDate(new Date());
  $('#curr').val(today);
}


function setupWeek(type)
	// date = yyyy-mm-dd
	{	
    // in prepation for the today tab - if it is on the current day, has this feature 
    	console.log('in setupweek');
      var editable = $('#schedule').data('editable');
      console.log(editable);
    	var groups = setGroups()
    	if (groups.length == 0) {
    		groups = 'None'
    	}
    	console.log(groups);
  		
    	 var active = document.getElementsByClassName('active')[0].id[1];
    	 console.log(active);
   		
		 var curr = $('#curr').val();
     console.log(curr);
     if (curr.trim() == "" || curr == null) {
      handleBadDate();
      curr = buildDate(new Date());
      $('#curr').val(curr);
     }
  
    
         let url = 'update';
         if (type == 'week') {
         	request = $.ajax(
              {
                 type: "GET",
                 url: url,
                 data: {
                  'newdate': curr,
             			'selectgroups': groups,
                  'editable':editable},
             	success: handleresponse,
               }
            );
         }
         else if (type == 'group') {
         request = $.ajax(
              {
                 type: "GET",
                 url: url,
                 data: {'newdate': curr,
             			'selectgroups': groups,
             			'groupday': active,
                  'editable':editable},
                 success: handleresponse,
               }
            );
     }
      else if (type =='nextweek') {
        curr = $('#d'+active).data('date');
        console.log(curr);
        var nextcurr = buildDate(new Date(new Date(curr).getTime()+(8*24*60*60*1000)));
        console.log(nextcurr);
        request = $.ajax(
              {
                 type: "GET",
                 url: url,
                 data: {
                  'newdate': nextcurr,
                  'selectgroups': groups,
                  'groupday': active,
                  'editable':editable},
              success: handleresponse,
               }
            );
      }
      else if (type =='lastweek') {
        curr = $('#d'+active).data('date');
        console.log(curr);
        var nextcurr = buildDate(new Date(new Date(curr).getTime()-(6*24*60*60*1000)));
        console.log(nextcurr);
        request = $.ajax(
              {
                 type: "GET",
                 url: url,
                 data: {
                  'newdate': nextcurr,
                  'selectgroups': groups,
                  'groupday': active,
                  'editable':editable},
              success: handleresponse,
               }
            );
      }

    }

function setGroups() {
	console.log('in set group');
	var groups = ""; 
    $("input:checkbox[name=selectGroups]:checked").each(addGroup)
    // a function handled for each needs to be index then item 
    function addGroup(index, item) { 
        groups += ($(item).val()) + '-';
     } 
     console.log(groups);
     return groups
}


function handleBadUser(msg) {
  $('#badUserMsg').html(msg);
  var modal = document.getElementById("handleBadUser");
  // $('#myModal').css('display','block');
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("closeBadUser");
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
    $("#selfname").val('');
    $("input[name='usertype']:checked").prop('checked', false); 
    document.getElementById("selectgroup").selectedIndex = 0;
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
      $("#selfname").val('');
      $("input[name='usertype']:checked").prop('checked', false); 
      document.getElementById("selectgroup").selectedIndex = 0;
      // make sure they are unchecked when we close 
    }
  }
  var ok = document.getElementById("okbad");
  ok.onclick = function() {
    modal.style.display = "none";
    $("#selfname").val('');
    $("input[name='usertype']:checked").prop('checked', false); 
    document.getElementById("selectgroup").selectedIndex = 0;
  }
}

// sendbook gathers all the stuff necessary to make a booking 
function sendbook(id) {
		// checks whether or not there are selected groups 
		console.log('in confirm');
		if (!$("input:radio[name='usertype']").is(":checked")) {
			console.log('bad');
			handleBadUser('No user selected. <br> <strong>Please check a user type: Self or Group</strong>');
      return;
		}
		var selectedUser = $("input[name='usertype']:checked").val();
        console.log(selectedUser);
        if (selectedUser == 'self') {
        	var user = encodeURIComponent($('#selfname').val());
          user.replace('<','&lt');
          user.replace('>','&gt');
        	if (user == "") {
        		handleBadUser('Self Booking: No name entered. <br> <strong>Please enter in your name</strong>');
        		return;
        	}
      
        }
        else {
        	if ($("#selectgroup option:selected").val() == "" || 
            $("#selectgroup option:selected").val() == "Select a group to book for") {
        		handleBadUser('Group Booking: No group selected. <br> <strong>Please select a group</strong>');
        		return;
        	}
        	var user = encodeURIComponent($("#selectgroup option:selected" ).val())
        	console.log(user);
        }
        user.replace('<','&lt');
        user.replace('>','&gt');
        var modal = document.getElementById("myModal");
        modal.style.display = "none"; 
        // uncheck this upon sending confirm
        $("input[name='usertype']:checked").prop('checked', false); 
        document.getElementById("selectgroup").selectedIndex = 0;
        // $("input[name='dgroup']:checked").prop('checked', false);
       	$("#selfname").val('');
        // splits from id and helps parse each detail 
        var info = id.split('.');
        console.log(info)
        // parse the studio and the after numbers
        var studioNum = info[0].match(/[a-z]+|[^a-z]+/gi); 
        console.log(studioNum);
        // what day is the booking occuring on 
        var day = Math.trunc(studioNum[1] % 10); 
        console.log(day)
        // start time of booking
        var hour = Math.trunc(studioNum[1] / 10);
        // gets name of the person who wants to book it 
        
        var date = info[1];
        console.log(date);
        console.log($('#curr').val());
        var currweek = $('#curr').val()

        var groups = setGroups()
      	if (groups.length == 0) {
      		groups = 'None'
      	}
    	  console.log(groups);

        var active = document.getElementsByClassName('active')[0].id[1];
       console.log(active);
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
                          'name': user, // name of person who is booking
                          'newdate': currweek, 
                          'selectgroups': groups, 
                          'groupday':active,

                      },
                      // upon ajax request callback
                      success: handleresponse,
                   }
                );
     }

function showConfirm(msg) {
	console.log('show confirm');
  var modal = document.getElementById("complete");
  $('#done').html(msg);
  modal.style.display = "block";

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
      // make sure they are unchecked when we close 
    }
  }
  var dismiss = document.getElementById("dismiss");
  dismiss.onclick = function() {
    modal.style.display = "none";
  }

}

// for displaying message that says they can delete this 
function del(event){
  console.log('show delete message');
  console.log(event.target.id);

}




function pastTime_drop(msg) {
  console.log('past the time error');
  $('#dropmsg').html(msg)
  // handles all modal - make it seen 
  var modal = document.getElementById("drop_errorPast");
 
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("drop_errorClose");
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

  // closing with oK button 
  var ok = document.getElementById("okbutton_drop");
  ok.onclick = function() {
    modal.style.display = "none";
  }
}


function handleDrop(event) {
  console.log('handle drop');
  var editable = $('#schedule').data('editable');
  console.log(editable);
  if (editable == 'False') {
      homeCannotBook(); 
      return;
  }

  var id = event.target.id;
  var end_time = $('#'+id).data('endtime');
  var booking_date = $('#'+id).data('bookingdate');
  // time error handling: cannot drop a previous space
  var dropped_date = new Date(booking_date);
  dropped_date.setHours(end_time);
  var today = new Date();
  if (dropped_date.getTime() < today.getTime()) {
    pastTime_drop('You cannot drop a time slot in the past. Please click on a time slot in the future');
    return;
  }
  var netid = $('#'+id).data('usernetid');
  var curruser = $('#netid').val();
  console.log(netid);
  console.log(curruser);
  if (netid != curruser) {
    console.log('you cannot drop this');
    pastTime_drop('You are not the booker of this space. You cannot drop/modify this time slot. ')
    return;
  }
  // handles all modal - make it seen 
  var modal = document.getElementById("confirmdrop");
 
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("confirmdropClose");
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

  // closing with oK button 
  var yes = document.getElementById("yesDrop");
  yes.onclick = function() {
    modal.style.display = "none";
    drop(event)
  }
  var no = document.getElementById("noDrop");
  no.onclick = function() {
    modal.style.display = "none";
    return false;
  }
}


function drop(event) {
  console.log('in drop');
  console.log(event);
  console.log('event target id' + event.target.id);
  
  var id = event.target.id;
  var company_name = encodeURIComponent($('#'+id).data('name'));
  var start_time = $('#'+id).data('starttime');
  var end_time = $('#'+id).data('endtime');
  var studio = $('#'+id).data('studio');
  var week_day = $('#'+id).data('weekday');
  var booking_date = $('#'+id).data('bookingdate');
  var currday =  $('#curr').val();
  console.log('dropping: ' + booking_date, studio, company_name, start_time, end_time, week_day);

  var groups = encodeURIComponent(setGroups())
  if (groups.length == 0) {
    groups = 'None';
  }
  console.log(groups);


  var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  console.log(csrftoken);

	
    console.log('user clicked ok');
    url = 'drop_space';
    request = $.ajax(
      {
         type: "POST",
         url: url,
         // headers: {'X-CSRFToken': '{{ csrf_token }}'}, // for csrf token
         headers: {'X-CSRFToken': csrftoken},
         data: {'studio': studio, // studio name 
             'date': booking_date, // in the form of Mon Day, Year
             'starttime': start_time, // int start time 
             'endtime': end_time, 
             'studio': studio,
             'day': week_day, // day of the week 
             'name': company_name, // name of person who is booking
             'selectgroups': groups,
             'currday': currday,
         },
         // upon ajax request callback
         success: handleresponse,
      }
   );
  showConfirm('Dropping completed!'); 
    
	} 
