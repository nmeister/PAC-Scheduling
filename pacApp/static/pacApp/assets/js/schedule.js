function book(id) {
	let col = id;
	console.log(col);
	var studioNum= col.match(/[a-z]+|[^a-z]+/gi);
	console.log(studioNum[0]);
	console.log(studioNum[1]);
	var day = studioNum[1] % 10; 
	var hour = studioNum[1] / 10;
	console.log(day);
	console.log(Math.trunc(hour));
	
}