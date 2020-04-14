function book(id) {
	console.log('booking')
	let col = id;
	console.log(col);
	var studioNum= col.match(/[a-z]+|[^a-z]+/gi);
	console.log(studioNum[0]);
	console.log(studioNum[1]);
	var day = studioNum[1] % 10; 
	var hour = studioNum[1] / 10;
	console.log(day);
	console.log(Math.trunc(hour));
	var modal = document.getElementById("myModal");
	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];
	modal.style.display = "block";

	window.onclick = function(event) {
  		if (event.target == modal) {
    		modal.style.display = "none";
  		}
  	}
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
	
}