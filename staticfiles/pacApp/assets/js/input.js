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

function validateResponse() 
{
  var empty_inputs = []
  let company = document.querySelector('input[name=company_name]').value.trim();
  let company_day_1 = document.querySelector('input[name=company_day_1]').value.trim();
  let company_studio_1 = document.querySelector('input[name=company_studio_1]').value.trim();
  let company_start_time_1 = document.querySelector('input[name=company_start_time_1]').value.trim();
  let company_end_time_1 = document.querySelector('input[name=company_end_time_1]').value.trim();

  let company_day_2 = document.querySelector('input[name=company_day_2]').value.trim();
  let company_studio_2 = document.querySelector('input[name=company_studio_2]').value.trim();
  let company_start_time_2 = document.querySelector('input[name=company_start_time_2]').value.trim();
  let company_end_time_2 = document.querySelector('input[name=company_end_time_2]').value.trim();

  let company_day_3 = document.querySelector('input[name=company_day_3]').value.trim();
  let company_studio_3 = document.querySelector('input[name=company_studio_3]').value.trim();
  let company_start_time_3 = document.querySelector('input[name=company_start_time_3]').value.trim();
  let company_end_time_3 = document.querySelector('input[name=company_end_time_3]').value.trim();

  let num_reho = document.querySelector('input[name=num_reho]').value.trim();
  let num_members = document.querySelector('input[name=num_members]').value.trim();

  let rank1s = document.querySelector('input[name=rank1s]').value.trim();
  let rank2s = document.querySelector('input[name=rank2s]').value.trim();
  let rank3s = document.querySelector('input[name=rank3s]').value.trim();
  let rank4s = document.querySelector('input[name=rank4s]').value.trim();
  let rank5s = document.querySelector('input[name=rank5s]').value.trim();

  if (company=="") empty_inputs.push('Company Name');
  if (company_day_1=="") empty_inputs.push('Company Day (Choice 1)');
  if (company_studio_1=="") empty_inputs.push('Company Studio (Choice 1)');
  if (company_start_time_1=="") empty_inputs.push('Company Start Time (Choice 1)');
  if (company_end_time_1=="") empty_inputs.push('Company End Time (Choice 1)');

  if (company_day_2=="") empty_inputs.push('Company Day (Choice 2)');
  if (company_studio_2=="") empty_inputs.push('Company Studio (Choice 2)');
  if (company_start_time_2=="") empty_inputs.push('Company Start Time (Choice 2)');
  if (company_end_time_2=="") empty_inputs.push('Company End Time (Choice 2)');

  if (company_day_3=="") empty_inputs.push('Company Day (Choice 3)');
  if (company_studio_3=="") empty_inputs.push('Company Studio (Choice 3)');
  if (company_start_time_3=="") empty_inputs.push('Company Start Time (Choice 3)');
  if (company_end_time_3=="") empty_inputs.push('Company End Time (Choice 3)');

  if (num_reho=="") empty_inputs.push('Number of Rehearsals Needed');
  if (num_members=="") empty_inputs.push('Number of Members');
  
  if (rank1s=="") empty_inputs.push('First Choice Studio');
  if (rank2s=="") empty_inputs.push('Second Choice Studio');
  if (rank3s=="") empty_inputs.push('Third Choice Studio');
  if (rank4s=="") empty_inputs.push('Fourth Choice Studio');
  if (rank5s=="") empty_inputs.push('Fifth Choice Studio');

  console.log(empty_inputs);

  if (empty_inputs != [])
  {
    console.log("This form did not submit");
    let alert_msg = "This form did not submit. Please fill in the following blanks: ";
    alert_msg += empty_inputs;
    alert(alert_msg);
    return false;
  }	
  return true;
}