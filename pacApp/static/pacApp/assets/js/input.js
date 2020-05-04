function openTab(evt, tab) {
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

function radio_check(radiobtn_name)
{
  var radios = document.getElementsByName(radiobtn_name);
  var i = 0;
  while (i < radios.length) {
    if (radios[i].checked) return "radio has value";
    i++;        
  }
  return ""
} 

function bad_company_time(start, end)
{
  console.log('start: ', start, 'end:', end);
  if (end <= start) return 'true';
  else return 'false';
}

function hasDuplicates(array) {
  return (new Set(array)).size !== array.length;
}

function rankingCheck(bloomberg_rank, dillon_dance_rank, dillon_mar_rank, dillon_mpr_rank, murphy_rank, ns_rank, ns_warmup_rank, ns_theatre_rank, whitman_rank, wilcox_rank) {
  var ranking_list = [bloomberg_rank, dillon_dance_rank, dillon_mar_rank, dillon_mpr_rank, murphy_rank, ns_rank, ns_warmup_rank, ns_theatre_rank, whitman_rank, wilcox_rank];
  console.log(hasDuplicates(ranking_list));
  if (hasDuplicates(ranking_list)) return "not unique";
  else return "unique";
}

function alphanumeric(inputtxt) {
  var letters = /^[0-9a-zA-Z]+$/;
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

// Ensure company 1 is different form company 2. return true if they are not unique
// company_1 is a list. company_1 = [company_day_1, company_studio_1, company_start_time_1, company_end_time_1]
function same_company(company_1, company_2)
{
  if ((company_1[0] == company_2[0]) && (company_1[1] != company_2[1]) && 
  (company_1[2] != company_2[2]) && (company_1[3] != company_2[3]))
  {
    return true;
  }
  else {return false;}
}

function validateResponse() 
{
  var empty_inputs = []
  let company = document.querySelector('input[name=company_name]').value.trim();

  let company_day_1 = radio_check('company_day_1') // 
  let company_studio_1 = radio_check('company_studio_1'); //
  let company_start_time_1 = document.querySelector('input[name=company_start_time_1]').value.trim();
  let company_end_time_1 = document.querySelector('input[name=company_end_time_1]').value.trim();

  let company_day_2 = radio_check('company_day_2') // 
  let company_studio_2 = radio_check('company_studio_2'); //
  let company_start_time_2 = document.querySelector('input[name=company_start_time_2]').value.trim();
  let company_end_time_2 = document.querySelector('input[name=company_end_time_2]').value.trim();

  let company_day_3 = radio_check('company_day_3') // 
  let company_studio_3 = radio_check('company_studio_3'); //
  let company_start_time_3 = document.querySelector('input[name=company_start_time_3]').value.trim();
  let company_end_time_3 = document.querySelector('input[name=company_end_time_3]').value.trim();

  let num_reho = document.querySelector('input[name=num_reho]').value.trim();
  let num_members = document.querySelector('input[name=num_members]').value.trim();

  let bloomberg_rank = document.querySelector('input[name=bloomberg_rank]').value.trim();
  let dillon_dance_rank = document.querySelector('input[name=dillon_dance_rank]').value.trim();
  let dillon_mar_rank = document.querySelector('input[name=dillon_mar_rank]').value.trim();
  let dillon_mpr_rank = document.querySelector('input[name=dillon_mpr_rank]').value.trim();
  let murphy_rank = document.querySelector('input[name=murphy_rank]').value.trim();
  let ns_rank = document.querySelector('input[name=ns_rank]').value.trim();
  let ns_warmup_rank = document.querySelector('input[name=ns_warmup_rank]').value.trim();
  let ns_theatre_rank = document.querySelector('input[name=ns_theatre_rank]').value.trim();
  let whitman_rank = document.querySelector('input[name=whitman_rank]').value.trim();
  let wilcox_rank = document.querySelector('input[name=wilcox_rank]').value.trim(); 

  if (company=="") empty_inputs.push('Company Name');

  if (company_day_1=="") empty_inputs.push('Company Day (Preference 1)'); //
  if (company_studio_1=="") empty_inputs.push('Company Studio (Preference 1)');//
  if (company_start_time_1=="") empty_inputs.push('Company Start Time (Preference 1)');
  if (company_end_time_1=="") empty_inputs.push('Company End Time (Preference 1)');

  if (company_day_2=="") empty_inputs.push('Company Day (Preference 2)');//
  if (company_studio_2=="") empty_inputs.push('Company Studio (Preference 2)');//
  if (company_start_time_2=="") empty_inputs.push('Company Start Time (Preference 2)');
  if (company_end_time_2=="") empty_inputs.push('Company End Time (Preference 2)');

  if (company_day_3=="") empty_inputs.push('Company Day (Preference 3)');//
  if (company_studio_3=="") empty_inputs.push('Company Studio (Preference 3)');//
  if (company_start_time_3=="") empty_inputs.push('Company Start Time (Preference 3)');
  if (company_end_time_3=="") empty_inputs.push('Company End Time (Preference 3)');

  if (num_reho=="") empty_inputs.push('Number of Rehearsals Needed');
  if (num_members=="") empty_inputs.push('Number of Members');
  
  if (bloomberg_rank=="") empty_inputs.push('Bloomberg Rank');
  if (dillon_dance_rank=="") empty_inputs.push('Dillon Dance Rank');
  if (dillon_mar_rank=="") empty_inputs.push('Dillon MAR Rank');
  if (dillon_mpr_rank=="") empty_inputs.push('Dillon MPR Rank');
  if (murphy_rank=="") empty_inputs.push('Murphy Rank');
  if (ns_rank=="") empty_inputs.push('NS Rank');
  if (ns_warmup_rank=="") empty_inputs.push('NS Warmup Rank');
  if (ns_theatre_rank=="") empty_inputs.push('NS Theatre Rank');
  if (whitman_rank=="") empty_inputs.push('Whitman Rank');
  if (wilcox_rank=="") empty_inputs.push('Wilcox Rank'); 

  console.log(empty_inputs);

  company_1 = [company_day_1, company_studio_1, company_start_time_1, company_end_time_1];
  company_2 = [company_day_2, company_studio_2, company_start_time_2, company_end_time_2];
  company_3 = [company_day_3, company_studio_3, company_start_time_3, company_end_time_3];

  // ensure that the company 1 and 2 entries are unique
  if (same_company(company_1, company_2)) {
    alert('Company preferences must be unique. Company 1 Preference is the same as the Company 2 preference.');
    return false;
  }

  if (same_company(company_1, company_3)) {
    alert('Company preferences must be unique. Company 1 Preference is the same as the Company 3 preference.');
    return false;
  }

  if (same_company(company_2, company_3)) {
    alert('Company preferences must be unique. Company 2 Preference is the same as the Company 3 preference.');
    return false;
  }
  
  // ensure company name is alphanumerics
  if (!alphanumeric(company)) {
    alert('Company name contains an incorrect character that is not a letter or a number. Please enter a valid company name.')
    return false;
  }
  
  // Ensure studio rankings are unique
  if (rankingCheck(bloomberg_rank, dillon_dance_rank, dillon_mar_rank, dillon_mpr_rank, murphy_rank, ns_rank, ns_warmup_rank, ns_theatre_rank, whitman_rank, wilcox_rank) == "not unique") {
    alert("The studio rankings are not unique. Please ensure that the numbers you've entered are different numbers for each box. Please fix your rankings and submit again.");
    return false;
  }

  // if any entry is empty
  else if (empty_inputs.length != 0)
  {
    console.log("This form did not submit");
    let alert_msg = "This form did not submit. Please fill in the following blanks: "
    alert_msg += empty_inputs;
    alert(alert_msg);
    return false;
  }	

  // if the start time of one is after the end time
  else if (bad_company_time(company_start_time_1, company_end_time_1)=='true'){
    alert('The end time for the company preference 1 is before the start time for company preference 1');
    return false;
  }
  else if (bad_company_time(company_start_time_2, company_end_time_2)=='true'){
    alert('The end time for the company preference 2 is before the start time for company preference 2');
    return false;
  }
  else if (bad_company_time(company_start_time_3, company_end_time_3)=='true'){
    alert('The end time for the company preference 3 is before the start time for company preference 3');
    return false;
  }
  /* add code here for error validation!! */
  else return true;
}

function wasClicked_Alg(event, type)
{
/*
  var start_date = document.querySelector('input[type=start_date]').value.trim();
  var end_date = document.querySelector('input[name=end_date]').value.trim();
  var start_dateArr = start_date.split('-');
  var end_dateArr = start_date.split('-');

  start_date = new Date(start_dateArr[0], start_dateArr[1], end_dateArr[2]);
  start_date = new Date(end_dateArr[0], end_dateArr[1], end_dateArr[2]);

  console.log(start_date, end_date);

  if (start_date > end_date) 
  {
    alert('The start date occurs after the end date. Please fix the dates and resubmit.');
    event.preventDefault();
    return false; 
  } */

  var ad_requests = "{{all_requests}}";
  console.log(ad_requests);


  if (jQuery.isEmptyObject(ad_requests))
  {
    alert('There are no entries in the AD request table. Please complete the form in Step 1 and ensure there is at least one entry in the table in Step 2 before proceding to allocate spaces.')
    return false;
  }

  schedule_wasClicked = localStorage.getItem('schedule_wasClicked');

  if(schedule_wasClicked=='true' && (type == "schedule")) { 
    console.log('show alert for schedule alg');
    console.log(event);
    alert('The PAC groups have already been scheduled. Please delete them before rescheduling.');
    event.preventDefault();
    return false; 
  }
  else if (type=='schedule')
  {
    console.log('proceed to scheduling alg');
    console.log(event);
    var schedule_wasClicked = "true";
    localStorage.setItem("schedule_wasClicked", schedule_wasClicked);
    return true;
  }  
  // change was clicked to false
  else if (schedule_wasClicked=='true' && (type == "delete")) {
    console.log('was clicked and now imma delete');
    var schedule_wasClicked = "false";
    localStorage.setItem("schedule_wasClicked", schedule_wasClicked);
    return true;
  }
  else if (schedule_wasClicked=='false' && (type == "delete")) {
    console.log('not was clicked and want to delete but nothing to del')
    alert('The PAC groups have not been schedule yet and there is nothing to delete. Please click "Schedule All Groups" First');
    event.preventDefault();
    return false;
  }

}
function handleresponse(response) 
{
	console.log('handle after update');
  $('.entire_page').html(response);
}

function validate_deleten(name)
{
  alert('Are you sure you want to delete ')
}



function delete_ad_request(name)
{
  let url = 'drop_ad_request';
  request = $.ajax(
              {
                type: "GET",
                url: url,
                data: {
                    'company_name': name, // name of group to drop
                },
                // upon ajax request callback
                success: handleresponse,
              }
          );

}
