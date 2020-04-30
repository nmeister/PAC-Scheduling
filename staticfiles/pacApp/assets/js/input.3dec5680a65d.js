
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
  if (end < start) return 'true';
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

  if (company_day_1=="") empty_inputs.push('Company Day (Choice 1)'); //
  if (company_studio_1=="") empty_inputs.push('Company Studio (Choice 1)');//
  if (company_start_time_1=="") empty_inputs.push('Company Start Time (Choice 1)');
  if (company_end_time_1=="") empty_inputs.push('Company End Time (Choice 1)');

  if (company_day_2=="") empty_inputs.push('Company Day (Choice 2)');//
  if (company_studio_2=="") empty_inputs.push('Company Studio (Choice 2)');//
  if (company_start_time_2=="") empty_inputs.push('Company Start Time (Choice 2)');
  if (company_end_time_2=="") empty_inputs.push('Company End Time (Choice 2)');

  if (company_day_3=="") empty_inputs.push('Company Day (Choice 3)');//
  if (company_studio_3=="") empty_inputs.push('Company Studio (Choice 3)');//
  if (company_start_time_3=="") empty_inputs.push('Company Start Time (Choice 3)');
  if (company_end_time_3=="") empty_inputs.push('Company End Time (Choice 3)');

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
  

  if (rankingCheck(bloomberg_rank, dillon_dance_rank, dillon_mar_rank, dillon_mpr_rank, murphy_rank, ns_rank, ns_warmup_rank, ns_theatre_rank, whitman_rank, wilcox_rank) == "not unique") {
    alert("The studio rankings are not unique. Please ensure that the numbers you've entered are different numbers for each box. Please fix your rankings and submit again.");
    return false;
  }
  else if (empty_inputs.length != 0)
  {
    console.log("This form did not submit");
    let alert_msg = "This form did not submit. Please fill in the following blanks: "
    alert_msg += empty_inputs;
    alert(alert_msg);
    return false;
  }	
  else if (bad_company_time(company_start_time_1, company_end_time_1)=='true'){
    alert('The end time for the company choice 1 is before the start time for company choice 1');
    return false;
  }
  else if (bad_company_time(company_start_time_2, company_end_time_2)=='true'){
    alert('The end time for the company choice 2 is before the start time for company choice 2');
    return false;
  }
  else if (bad_company_time(company_start_time_3, company_end_time_3)=='true'){
    alert('The end time for the company choice 3 is before the start time for company choice 3');
    return false;
  }
  else if (num_reho > 50) {
    alert('This group requested too many rehearsal spaces. Please lower the number to below 50 spaces per week.');
    return false;
  }
  else return true;
}

function wasClicked_Alg(event, type)
{

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
  $('#ad_results_table').html(response);
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