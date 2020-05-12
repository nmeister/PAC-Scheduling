function openDay(tab, id) {
   if (window.refresh != null) {
    clearInterval(window.refresh);
    window.refresh = setInterval(function () {
          setupWeek('group');}
          , 7000);
          console.log('window', window.refresh); 
  }
  // opens the tab content corresponding to clicked tab
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
  // for each of the tabs, make them all display none
  for (i = 0; i < 7; i++) {
  	 $('#d'+i+'date').css('display','none');
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tab).style.display = "block";
  document.getElementById(id).className += " active";
  var weekdays= {'sun':0,'mon':1,'tue':2,'wed':3,'thu':4,'fri':5,'sat':6};
  var date = $('#'+id).data('date').split('-');
  console.log('opened on this date:' + date)
  var reformatted = date[1] + '/' + date[2] + '/' + date[0].substring(2,4); 
  // console.log(date[0].substring(2));
  // console.log(date[0].substring(2));
  $('#'+id+'date').html(reformatted);
  $('#'+id+'date').css('display','block');
  $('#curr').val($('#'+id).data('date')); 

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

function setGroups() {
  console.log('in set group');
  var groups = ""; 
  $("input:checkbox[name=selectGroups]:checked").each(addGroup)
  // a function handled for each needs to be index then item 
  function addGroup(index, item) { 
    groups += ($(item).val()) + '-';
  } 
  console.log(groups);
  if (groups.length == 0) {
    return 'None';
  }
  return groups;
}


function handleBadDate() {
  console.log('handling a bad date modal');
  
  // handles all modal - make it seen 
  var msg = '<strong> Please enter a valid date </strong> . <br> Earliest possible is 12/31/2000.';
  $('#errorMsg').html(msg);
  var modal = document.getElementById("errorModal");
  // Get the <span> element that closes the modal on the x button 
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

  var ok = document.getElementById("one");
  $('#one').html('OK');
  $('#two').css('display','none');
  ok.onclick = function() {
    $('#errorModal').css('display','none');
    $('#two').css('display','inline-block');
  }

}

function handleWeekInput() {

  var timeout = null              //timer identifier
  var doneTypingInterval = 3000;  //time in ms (2 seconds)

  //on keyup, start the countdown
  $('#curr').attr('onkeyup', function (e) {
    // Clear the timeout if it has already been set.
    // This will prevent the previous task from executing
    // if it has been less than <MILLISECONDS>
    clearTimeout(timeout);

    // Make a new timeout set to go off in 1000ms (1 second)
    timeout = setTimeout(doneTyping, doneTypingInterval);
  });
}


//user is "finished typing," do something
function doneTyping () {
    console.log("done typing");
    //do something
    var currweek = $('#curr').val();
    console.log(currweek);
    var currdate = new Date(currweek);
    console.log(currdate)
    var earliestPossible = new Date(2000, 12, 31).getTime();
    var latestPossible = new Date(2500, 12, 31).getTime();
    if (currdate.getTime() > latestPossible || currdate.getTime() < earliestPossible) {
      console.log('handling bad date');
      handleBadDate();
      var today = buildDate(new Date());
      $('#curr').val(today);
    }
    setupWeek('week');
    return;
}

// UPDATING THE CALENDAR 
function setupWeek(type) {
  console.log('in update week calendar');
  var groups = setGroups();

  console.log('type of call is: ' + type);
  
  // if by clicking on the date picker
  if (type == 'week') {
    var newdate = $('#curr').val();
    console.log('updating week to be: ' + newdate);
    let url = 'updateWeek';
    request = $.ajax(
    {
      type: "GET",
      url: url,
      data: {
        'newdate': newdate,
        'groups': groups,
      },
      success: handleresponse,
    })
    ;
  }
  // by clicking the forward arrow 
  if (type == 'nextweek') {
    var currweek = $('#curr').val();
    nextdate = buildDate(new Date(new Date(currweek).getTime()+(8*24*60*60*1000)));
    console.log('the next week starts on: ' + nextdate);
    let url = 'updateWeek';
    request = $.ajax(
    {
      type: "GET",
      url: url,
      data: {
        'newdate': nextdate,
        'groups': groups,
      },
      success: handleresponse,
    })
    ;
  }
  // by clicking the backward arrow
  if (type == 'lastweek') {
    // var active = document.getElementsByClassName('active')[0].id[1];
    // console.log(active);
    // var openeddate = $('#d'+active).data('date');
    var currweek = $('#curr').val();
    nextdate = buildDate(new Date(new Date(currweek).getTime()-(6*24*60*60*1000)));
    console.log('the lastweek starts on: ' + nextdate);
    let url = 'updateWeek';
    request = $.ajax(
    {
      type: "GET",
      url: url,
      data: {
        'newdate': nextdate,
        'groups': groups,
      },
      success: handleresponse,
    })
    ;
  }

  if (type == 'group') {
    // var active = document.getElementsByClassName('active')[0].id[1];
    // console.log('active day is ' + active);
    // var openeddate = $('#d'+active).data('date');
    var currweek = $('#curr').val();
    console.log('current week starts on: ' + currweek);
    let url = 'updateGroupOnly';
    request = $.ajax(
    {
      type: "GET",
      url: url,
      data: {
        'openday': currweek,
        'currweek': currweek,
        'groups': groups,
      },
      success: handleresponse,
    })
    ;
  }
   if (window.refresh != null) {
    clearInterval(window.refresh);
    window.refresh = setInterval(function () {
          setupWeek('group');}
          , 7000);
          console.log('window setupweek', window.refresh); 
  }  
}


function handleresponse(response) 
{
  console.log('handle after update');
  // updates the calendar
  $('#schedule').html(response);
}

// Checks where we are, if not schedule page, don't allow booking 
function homeCannotBook() {
  console.log('home cannot book error');
  var user = $('#scheduleOnHome').data('user');
  console.log('user from home is: ' + user);
  var msg = 'You are not allowed to book or drop spaces on this page. <br><strong>  Please login to do so. </strong> ';
  var buttonText = 'LOGIN';
  if (user != 'None') {
    msg = 'You are not allowed to book or drop spaces on this page. <br> <strong> Please click on the button to go to booking page.</strong> '
    buttonText = 'BOOKING PAGE';
  }
  // handles all modal - make it seen 
  var modal = document.getElementById("errorModal");
  modal.style.display = "block";
  $('#errorMsg').html(msg);

  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("errorClose");
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
  var option = document.getElementById("two");
  $('#two').html(buttonText);
  $('#one').css('display','none');
  option.onclick = function() {
    modal.style.display = "none";
    location.href = "schedule";
    $('#one').css('display','inline-block');
  }
}


// if we are within current hour and they still want to book 
function withinCurrentHourBooking(left, id) {
  console.log('within current hour booking');
  var msg = 'You only have <span>' + left + '</span> minutes left for this time slot. <br> <strong> Do you want to continue booking?</strong> ';
  $('#errorMsg').html(msg);
  // handles all modal - make it seen 
  var modal = document.getElementById("errorModal");
 
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
  $('#one').css('display','inline-block');
  $('#two').css('display','inline-block');
  $('#one').html('YES');
  $('#two').html('NO');
  var yes = document.getElementById("one");
  var no = document.getElementById("two");
  var multi = $('#scheduletable').data('multi');
  yes.onclick = function() {
    modal.style.display = "none";
    console.log('continue booking');
    if (multi == 0) {
      book(id);
    }
    else if (multi == 1) {
      bookmulti(id);
    }
  }

  no.onclick = function() {
     modal.style.display = "none";
     console.log('dont wanna book');
     return;
  }
}


function pastTime() {
  console.log('past the time error modal');
  
  // handles all modal - make it seen 
  var msg = 'You cannot book a time slot in the past. <br> <strong> Please click on a time slot in the future. </strong> ';
  $('#errorMsg').html(msg);
  var modal = document.getElementById("errorModal");
  // Get the <span> element that closes the modal on the x button 
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

  var ok = document.getElementById("one");
  $('#one').html('OK');
  $('#two').css('display','none');
  ok.onclick = function() {
    $('#errorModal').css('display','none');
    $('#two').css('display','inline-block');
  }
}

// checks for editing by place and time 
function canEdit(id) {
  console.log('id in canEdit' + id);
  var editable = 0;
  var place = String(window.location.pathname);
  // || place != "/schedule")  { can only happen on this page 
  if (place == "/" || place == "/homepage") {
    homeCannotBook(); 
    return;
  }
  else if (place == '/showResults') {
    editable = 1
    console.log('can book showresults');
  }
  else {
    editable = 1
    console.log('can book');
  }
  if ($('#' +id).data('selected') == 1) {
    console.log('selected');
    deleteSelected(id);
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
  console.log('todays date with hour:' + today);
  console.log('strict date with hour after' + strictdate);
  console.log('current right now' + today.getTime());
  console.log('this timeslot' + strictdate.getTime());

  var stillBook = 'no'
  var multi = $('#scheduletable').data('multi');
  console.log('multi', multi);
  if (strictdate.getTime() < today.getTime()) {
      if (today.getTime() - strictdate.getTime() < 55 * 60000) {
        console.log('still within 55 minutes');
        var minLeft = Math.trunc((nextHour.getTime() - today.getTime()) / 60000)
        var stillBook = withinCurrentHourBooking(minLeft, id);
        return;
      }
      editable = 0
  }
  if (editable == 1) {
      console.log('can book');
      if (multi == 0) {
        book(id);
      }
      else if (multi == 1) {
      // userInfoModalMulti(id);
      bookmulti(id);
      }
  }
  else {
      console.log('way past booking time');
      pastTime();
  }
}


function book(id) {

  console.log('parsing book id');
  let col = id;
  // console.log(col);
  var studioNum= col.match(/[a-z]+|[^a-z]+/gi);
  // console.log(studioNum[0])
  // console.log(studioNum[1]);
  var studio = studioNum[0]
  var day = studioNum[1] % 10; 
  var hour = studioNum[1] / 10;

  console.log(id);
  console.log('studio to be booked is: ' + studio);
  booking(studio,day,hour,id);
}

// USED TO FIND A NICELY FORMATTED NAME FOR STUDIO
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


function userInfoModal() {

   // handles all modal - make it seen 
  var modal = document.getElementById("myModal");
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("bookClose");
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    $('#self').prop("checked", false);
    $('#group').prop("checked", false);
    $("#selfname").val('');
    $("input[name='usertype']:checked").prop('checked', false); 
    document.getElementById("selectgroup").selectedIndex = 0;
    modal.style.display = "none";
    
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      // make sure they are unchecked when we close 
      $('#self').prop("checked", false);
      $('#group').prop("checked", false);
      $("#selfname").val('');
      $("input[name='usertype']:checked").prop('checked', false); 
      document.getElementById("selectgroup").selectedIndex = 0;
      modal.style.display = "none";
      
    }
  }
}

// PARSING AND GATHERING THE INFORMATION WE NEED FOR BOOKING
function booking(studio,day,hour,id) {
  console.log('hello @ booking');
  userInfoModal();
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
  
  
  var content = '#content' + day;
  console.log($(content).data('date'));
  var dateArr = $(content).data('date').split('-');
  console.log(dateArr);
  var date = new Date(dateArr[0], dateArr[1]-1, dateArr[2]);
  // still part of today so we want to make it in the db as same as today
  var datadate = date;
  // but technically it is tomorrow so 
  if (Math.trunc(hour) > 23) {
    var nextday = parseInt(dateArr[2]) + 1
    date = new Date(dateArr[0], dateArr[1]-1, nextday);
  }
  console.log(date);
  var bookdate = document.getElementById('bookdate');
  // console.log(date)
  bookdate.innerHTML = "Booking Day: " + date.toDateString();
  var currdate = new Date(dateArr[0], dateArr[1]-1, dateArr[2]);
  var nextdate = new Date(dateArr[0], dateArr[1]-1, parseInt(dateArr[2]) + 1);
  
  console.log($('#netid').data('user'));
  $('#personNet').html(' <strong>(' + $('#netid').data('user') + ')</strong>');
  var confirm = document.getElementById("confirm");
  // should have studio[start_time][dayofweek].yyyy-mm-dd
  confirm.value = id;
  confirm.value += '.';
  // dilliondance203.2020-04-15
  confirm.value += buildDate(datadate);
  console.log('confirmed value ', confirm.value)
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
    $("#selfname").val('');
    $("input[name='usertype']:checked").prop('checked', false); 
    document.getElementById("selectgroup").selectedIndex = 0;
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      $("#selfname").val('');
      $("input[name='usertype']:checked").prop('checked', false); 
      document.getElementById("selectgroup").selectedIndex = 0;
      modal.style.display = "none";
      // make sure they are unchecked when we close 
    }
  }
  var ok = document.getElementById("okbad");
  ok.onclick = function() {
    $("#selfname").val('');
    $("input[name='usertype']:checked").prop('checked', false); 
    document.getElementById("selectgroup").selectedIndex = 0;
    modal.style.display = "none";
    
  }
}

function allLetters(inputtxt) {
   var letters = /^[A-Za-z]+$/;
   if(inputtxt.match(letters))
     {
      return true;
     }
   else
     {
     console.log('bad name entered');
     return false;
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
    // if selected user is self
    if (selectedUser == 'self') {
      // var user = ($('#selfname').val());
      var user = $('#netid').data('user');
      var userid = 0;
      /*if (user == "") {
        handleBadUser('Self Booking: No name entered. <br> <strong>Please enter in your name</strong>');
        return;
      }
      if (allLetters(user) == false) {
        handleBadUser('Self Booking: Name should only have alphabet letters. <br><strong> Please enter in a valid name without spaces, numbers, or special characters.</strong>');
        return;
      }*/
    }
    else {
      if ($("#selectgroup option:selected").val() == "" || $("#selectgroup option:selected").val() == "Select a group to book for") {
        handleBadUser('Group Booking: No group selected. <br> <strong>Please select a group</strong>');
        return;
      }
      var userid = parseInt(($("#selectgroup option:selected" ).val()));
      var groups = ['BAC', 'Bhangra', 'BodyHype', 'diSiac', 'eXpressions', 'HighSteppers',
                        'KoKo Pops', 'Naacho', 'PUB', 'Six14', 'Sympoh', 'Triple 8'];
      var user = groups[userid-1];
    }

    var modal = document.getElementById("myModal");
    modal.style.display = "none"; 
    // uncheck this upon sending confirm
    $("input[name='usertype']:checked").prop('checked', false);

    document.getElementById("selectgroup").selectedIndex = 0;

    $("#selfname").val('');
    // THE FOLLOWING FOR SELECTED HOURS 
   /* var numhours = parseInt($('#nhours').val());
    if (numhours == null || numhours == '') {
      numhours = 1;
    }
    $('#nhours').val('');*/

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

    var currweek = $('#curr').val();

    var groups = setGroups();
    console.log(groups);

    // var active = document.getElementsByClassName('active')[0].id[1];
    // console.log(active);
    console.log('userid is ' + userid);
    console.log('user is ' + user);
    // var openday = $('#d'+active).data('date');
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let url = 'updateBooking';
    request = $.ajax(
    {
      type: "POST",
      url: url,
      headers: {'X-CSRFToken': csrftoken},
      data: {'studio': studioNum[0], // studio name 
             'date': date, // in the form of yyyy/mm/dd
             'starttime': hour, // int start time 
             'endtime': hour+1, 
             'day': day, // day of the week 
             'name': encodeURIComponent(user), // name of person who is booking
             'nameid': userid,
             'currweek': currweek,
             'groups': groups, 
             'openday': currweek,
           },
           // upon ajax request callback
           success: handleresponse,
         });
}


function showConfirm(msg) {
  console.log('show confirm');
  var modal = document.getElementById("errorModal");
  $('#errorMsg').html('<span style="font-size: 1em">' + msg + '</span>');
  modal.style.display = "block";


  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("errorClose");
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
  var dismiss = document.getElementById("one");
  $('#one').html('DISMISS');
  $('#two').css('display','none');
  dismiss.onclick = function() {
    $('#errorModal').css('display','none');
    $('#two').css('display','inline-block');
  }
}

function pastDrop(msg) {
  console.log('error while trying to drop');
  $('#errorMsg').html(msg)
  // handles all modal - make it seen 
  var modal = document.getElementById("errorModal");
 
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
  var ok = document.getElementById("two");
  $('#two').html('OK');
  $('#one').css('display','none');
  ok.onclick = function() {
    modal.style.display = "none";
    $('#one').css('display','inline-block');
  }
}


function handleDrop(event) {
  console.log('handle drop');
  var editable = 0
  var place = String(window.location.pathname);
  if (place == "/" || place == "/homepage")  {
      homeCannotBook(); 
      return;
  }
  else if (place == '/showResults') {
     editable = 1
      console.log('can drop show results');
  }
  else {
    editable = 1
    console.log('can drop schedule');
  }

  var id = event.target.id;
  var end_time = $('#'+id).data('endtime');
  var booking_date = $('#'+id).data('bookingdate');
  // time error handling: cannot drop a previous space
  var dropped_date = new Date(booking_date);
  dropped_date.setHours(end_time);
  var today = new Date();
  if (dropped_date.getTime() < today.getTime()) {
    pastDrop('You cannot drop a time slot in the past. <br> <strong> Please click on a time slot in the future. </strong>');
    return;
  }
  var netid = $('#'+id).data('usernetid');
  var curruser = $('#netid').data('user');
  console.log('booker netd' + netid);
  console.log('current person' + curruser);
  if (netid != curruser) {
    console.log('you cannot drop this');
    pastDrop('You are not the booker of this space. <br> <strong> You cannot drop/modify this time slot. </strong> ')
    return;
  }

  // ONCE WE MAKE SURE WE ARE ALLOWED TO DROP THIS
  // handles all modal - make it seen 
  var modal = document.getElementById("errorModal");
  $('#errorMsg').html('<strong> Are you sure you want to drop this space? </strong>');
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

  $('#one').html('YES');
  $('#two').html('NO');
  $('#one').css('display', 'inline-block');
  $('#two').css('display', 'inline-block');
  // closing with oK button 
  var yes = document.getElementById("one");
  yes.onclick = function() {
    modal.style.display = "none";
    drop(event)
  }
  var no = document.getElementById("two");
  no.onclick = function() {
    modal.style.display = "none";
    console.log('decided not to drop');
    return;
  }
}


// for displaying message that says they can delete this 
function del(event){
  console.log('show delete message');
  console.log(event.target.id);
  
}


function drop(event) {
  console.log('in drop');
  console.log(event);
  console.log('event target id' + event.target.id);
  var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  console.log('token is: ' + csrftoken);
  
  var id = event.target.id;
  var company_name = $('#'+id).data('name');
  var company_id = $('#'+id).data('nameid');
  var start_time = $('#'+id).data('starttime');
  var end_time = $('#'+id).data('endtime');
  var studio = $('#'+id).data('studio');
  var week_day = $('#'+id).data('weekday');
  var booking_date = buildDate(new Date($('#'+id).data('bookingdate')));
  var usernetid =  $('#'+id).data('usernetid');
  var currweek =  $('#curr').val();
  console.log('dropping: ' + booking_date, studio, company_name, company_name, start_time, end_time, week_day, usernetid);

  var active = document.getElementsByClassName('active')[0].id[1];
  console.log(active);
  var openday = $('#d'+active).data('date');

  var groups = setGroups();

  url = 'updateDropping';
    request = $.ajax(
      {
         type: "POST",
         url: url,
        
         headers: {'X-CSRFToken': csrftoken},
         data: {'studio': studio, // studio name 
             'date': booking_date, // in the form of Mon Day, Year
             'starttime': start_time, // int start time 
             'endtime': end_time, 
             'studio': studio,
             'day': week_day, // day of the week 
             'name': company_name, // name of person who is booking
             'nameid': company_id,
             'netid': usernetid,
             'groups': groups,
             'currweek': currweek,
             'openday': currweek,
         },
         // upon ajax request callback
         success: handleresponse,
      }
   );
}


function fwdbck() {
  $('#forward').attr('data-toggle',"tooltip");
  $('#forward').attr('data-placement', "top"); 
  $('#forward').data('delay', 0);
  $('#forward').attr('title', 'Click to see next week');
  $('#backward').attr('data-toggle',"tooltip");
  $('#backward').attr('data-placement', "top"); 
  $('#backward').data('delay', 0);
  $('#backward').attr('title', 'Click to see last week');
}



// MISCELLANEOUS FUNCTIONS 
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



function multiselect() {
  console.log('multiselect');
  $('#scheduletable').data('multi', 1);
  $('#bookingbutton').css('border', 'solid 0.2em lightblue');
  $('#bookingbutton').css('background-color', '#df7366');
  $('#bookingbutton').attr('onclick', 'deselect()');
  $('#bookingbutton').css('display','none');
  var confirm = '<span id="multiSub" class="button" style="padding:0.5em;margin:0.25em;font-size:0.8em" onclick="sendmultibook()">CONFIRM</span>';
  var cancel = '<span class="button" style="padding:0.5em;margin:0.25em;font-size:0.8em" onclick="deselect()">CANCEL</span>';
  $('#confirmMulti').html(confirm+cancel);
  if (window.refresh != null) {
    clearInterval(window.refresh);
    window.refresh = setInterval(function () {
          setupWeek('group');}
          , 5000);
          console.log('window', window.refresh);
  } 

}


function deselect() {
  var confirm = $('#multiSub').val().split('/');
  console.log(confirm);
  for (var i = 1; i < confirm.length; i++) {
    console.log(confirm[i])
    $('#'+confirm[i]).css('background-color','');
    $('#'+confirm[i]).data('selected',0);
  }
  $('#multiSub').data('users','');
  console.log('multisub-users is', $('#multiSub').data('users'));
  $('#multiSub').val('');
  $('#bookingbutton').attr('onclick', 'multiselect()');
  $('#bookingbutton').css('display','inline-block');
  $('#confirmMulti').html('');
  $('#bookingbutton').css('background-color', '#df7366');
  $('#bookingbutton').css('border', '');
  $('#scheduletable').data('multi', 0);
  $('#confirm').attr('onclick', 'sendbook(this.value)');
  
}



function bookmulti(id) {
  console.log(id);
  userInfoModalMulti(id)
  if (window.refresh != null) {
    clearInterval(window.refresh);
    window.refresh = setInterval(function () {
          setupWeek('group');}
          , 5000);
          console.log('window', window.refresh);
  } 
}

function userInfoModalMulti(id) {
  $('#personNetM').html('Net Id: <strong>' + $('#netid').data('user') + '</strong>')
   // handles all modal - make it seen 
  var modal = document.getElementById("multiModal");
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("multiClose");
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    $('#selfM').prop("checked", false);
    $('#groupM').prop("checked", false);
    $("#selfnameM").val('');
    $("input[name='usertypeM']:checked").prop('checked', false); 
    document.getElementById("selectgroupM").selectedIndex = 0;
    modal.style.display = "none";
    
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      // make sure they are unchecked when we close 
      $('#selfM').prop("checked", false);
      $('#groupM').prop("checked", false);
      $("#selfnameM").val('');
      $("input[name='usertypeM']:checked").prop('checked', false); 
      document.getElementById("selectgroupM").selectedIndex = 0;
      modal.style.display = "none";
      
    }
  }

  var ok = document.getElementById("confirmOne");
  ok.onclick = function() {
    console.log('to add user');
    addUser(id);

  }
}

function handleBadUserM(msg) {
  $('#badUserMsgM').html(msg);
  var modal = document.getElementById("handleBadUserM");
  // $('#myModal').css('display','block');
  // Get the <span> element that closes the modal on the x button 
  var span = document.getElementById("closeBadUserM");
  modal.style.display = "block";
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    $("#selfnameM").val('');
    $("input[name='usertypeM']:checked").prop('checked', false); 
    document.getElementById("selectgroupM").selectedIndex = 0;
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      $("#selfnameM").val('');
      $("input[name='usertypeM']:checked").prop('checked', false); 
      document.getElementById("selectgroupM").selectedIndex = 0;
      modal.style.display = "none";
      // make sure they are unchecked when we close 
    }
  }
  var ok = document.getElementById("okbadM");
  ok.onclick = function() {
    $("#selfnameM").val('');
    $("input[name='usertypeM']:checked").prop('checked', false); 
    document.getElementById("selectgroupM").selectedIndex = 0;
    modal.style.display = "none";
    
  }
}

function addUser(id) {
  console.log('adding user');
  if (!$("input:radio[name='usertypeM']").is(":checked")) {
      console.log('bad');
      handleBadUserM('No user selected. <br> <strong>Please check a user type: Self or Group</strong>');
      return;
    }
    var selectedUser = $("input[name='usertypeM']:checked").val();
    console.log(selectedUser);
    // if selected user is self
    if (selectedUser == 'selfM') {
      var user = $('#netid').data('user');
      console.log(user);
      var userid = 0;
      /*if (user == "") {
        handleBadUserM('Self Booking: No name entered. <br> <strong>Please enter in your name</strong>');
        return;
      }
      if (allLetters(user) == false) {
        handleBadUserM('Self Booking: Name should only have alphabet letters. <br><strong> Please enter in a valid name without spaces, numbers, or special characters.</strong>');
        return;
      }
    } */ 
    }
    else {
      if ($("#selectgroupM option:selected").val() == "" || $("#selectgroupM option:selected").val() == "Select a group to book for") {
        console.log(user);
        handleBadUserM('Group Booking: No group selected. <br> <strong>Please select a group</strong>');
        return;
      }
      var userid = parseInt(($("#selectgroupM option:selected" ).val()));
      var groups = ['BAC', 'Bhangra', 'BodyHype', 'Disiac', 'eXpressions', 'HighSteppers',
                        'Kokopops', 'Naacho', 'PUB', 'Six14', 'Sympoh', 'Triple8'];
      var user = groups[userid-1];
    }

    var modal = document.getElementById("multiModal");
    modal.style.display = "none"; 
    // uncheck this upon sending confirm
    $("input[name='usertypeM']:checked").prop('checked', false);

    document.getElementById("selectgroupM").selectedIndex = 0;

  $("#selfnameM").val('');
  console.log(user);
  console.log(userid);
  var currUsers =  $('#multiSub').data('users');
  $('#multiSub').data('users', currUsers + '/' + user + '-' + userid);
  console.log($('#multiSub').data('users'));
  $('#'+id).css('background-color','pink');
  $('#'+id).data('selected',1);
  $('#multiSub').val($('#multiSub').val() + '/' + id );
}

function sendmultibook() {
  console.log('in multisend book ', $('#multiSub').val());
  var slots = $('#multiSub').val().split('/');
  console.log(slots);
  var slotsinfo = [];
  var netid = $('#netid').data('user');
  var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  console.log($('#multiSub').data('users'));
  var allUsers =  $('#multiSub').data('users').split('/');
  // allUsers.shift();
  console.log('all users in sendmulti', allUsers);
  slots.forEach(parseId, slotsinfo);
  function parseId(item, index, arr) {
    if (item != '') {
      console.log(item);
      var studioNum= item.match(/[a-z]+|[^a-z]+/gi);
      var studio = studioNum[0]
      var day = studioNum[1] % 10; 
      var hour = studioNum[1] / 10;
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
      slotsinfo.push({
         company_name:allUsers[index].split('-')[0],
         company_id:allUsers[index].split('-')[1],
         start_time:hour,
         end_time:hour+1,
         studio:studio,
         week_day:day,
         booking_date:buildDate(date),
         user_netid:netid,
        })
    }
  }
  var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  console.log('before request', slotsinfo);
  var currweek =  $('#curr').val();
  var active = document.getElementsByClassName('active')[0].id[1];
  console.log(active);
  var openday = $('#d'+active).data('date');
  var groups = setGroups();
  deselect();
  url = 'updateMulti';
  request = $.ajax(
  {
    type: "POST",
    url: url,
    headers: {'X-CSRFToken': csrftoken},
    data: {
      'slots[]': JSON.stringify(slotsinfo),
      'openday':openday,
      'currweek':currweek,
      'groups':groups
    },
    success: handleresponse,
  });
}

function removeElement(array, elem) {
    var index = array.indexOf(elem);
    console.log(index);
    if (index > -1) {
        array.splice(index, 1);
    }
}

function deleteSelected(id) {
  var confirm = $('#multiSub').val().split('/');
  removeElement(confirm, id);
  $('#multiSub').val(confirm.join('/'));
  console.log($('#multiSub').val());
  $('#'+id).css('background-color','');
  $('#'+id).data('selected',0);
}