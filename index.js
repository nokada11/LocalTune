var blink_speed = 1000; // every 1000 == 1 second, adjust to suit
var t = setInterval(function () {
	var ele = document.getElementById('title');
	ele.style.visibility = (ele.style.visibility == 'hidden' ? '' : 'hidden');
}, blink_speed);

var el = document.getElementById('title');
// el.addEventListener("click", modifyText());

// function modifyText() {
// 			var title = document.getElementById('playing');
// 			title.innerHTML = "Hi...";
// }

document.getElementById("myBtn").addEventListener("click", displayDate);

function displayDate() {
	document.getElementById("date").innerHTML = Date();
}




