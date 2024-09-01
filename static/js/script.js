
$(document).ready(function(){

	startclock()

});

function startclock(){
	var timerID = null
	var timerRunning = false
	stopclock(timerID, timerRunning)
	showtime(timerID, timerRunning)
	}

function stopclock(timerID, timerRunning){
	if (timerRunning) 
		clearTimerout(timerID)
	timerRunning = false
	}

function showtime(timerID, timerRunning){
	var data_n = new Date()
	locale = "pl-PL"
	var x = data_n.toLocaleString(locale,{weekday: "long"})
	var y = x.charAt(0).toUpperCase() + x.slice(1);
	var godz = data_n.getHours()
	var min = data_n.getMinutes()
	var sek = data_n.getSeconds()
	var czas = y + ", " + (godz)
	czas += ((min<10) ? ":0" : ":") +min
	czas += ((sek<10) ? ":0" : ":") +sek
	document.getElementById('clock').innerHTML = czas
	timerID = setTimeout("showtime()",1000)
	timerRunning = true
}

// Sidebar resize script
$(document).ready(function() {
    const sidebar = document.querySelector('.content-section > section');
    const content = document.querySelector('.content-wrapper');
    const mainContainer = document.querySelector('.content-section');
    const footer = document.querySelector('#footer');
    const margin = 80; // Adjust this value as needed

	// Delay the logging to ensure styles are computed
    setTimeout(() => {
        console.log(mainContainer);
        const computedStyles = window.getComputedStyle(mainContainer);
        console.log(computedStyles);
        console.log(computedStyles.marginBottom);

        if (content.offsetHeight > window.innerHeight) {
            sidebar.style.height = (content.offsetHeight) + 'px';
        } else {
            sidebar.style.height = (content.offsetHeight) + 'px';
            const contentMargin = parseInt(computedStyles.marginBottom);
            sidebar.style.height = (content.offsetHeight + contentMargin) + 'px';
        }
    }, 1);
});

// Messages offset script
document.addEventListener('DOMContentLoaded', function() {
    const navbarHeight = document.querySelector('.navbar').offsetHeight;
    document.getElementById('messages-section').style.marginTop = (navbarHeight + 6) + 'px';
});