const cookieStorage = {
    getItem: (key) => {
        const cookies = document.cookie
            .split(';')
            .map(cookie => cookie.split('='))
            .reduce((acc, [key, value]) => ({ ...acc, [key.trim()]: value }), {});
        return cookies[key];
    },
    setItem: (key, value) => {
        document.cookie = `${key}=${value}; expires=Thu, 31 Dec 2055 12:00:00 UTC; path=/`
    }
}

const storageType = cookieStorage;
const consentPropertyName = 'cookie_consent';

const shouldShowPopup = () => !storageType.getItem(consentPropertyName);
const saveToStorage = () => storageType.setItem(consentPropertyName, true);

window.onload = () => {
    const consentPopup = document.getElementById('consent-popup');
    const acceptBtn = document.getElementById('accept');

    const acceptFn = event => {
        saveToStorage(storageType);
        consentPopup.classList.add('hidden');
    }

    acceptBtn.addEventListener('click', acceptFn);

    if (shouldShowPopup(storageType)) {
        setTimeout(() => {
            consentPopup.classList.remove('hidden');
        }, 1000);
    }

};

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