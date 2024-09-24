
// Sidebar resize script
$(document).ready(function() {
    const sidebar = document.querySelector('.content-section > section');
    const content = document.querySelector('.content-wrapper');
    const mainContainer = document.querySelector('.content-section');

	// Delay the logging to ensure styles are computed
    if (sidebar) {
        setTimeout(() => {
            const computedStyles = window.getComputedStyle(mainContainer);

            if (content.offsetHeight > window.innerHeight) {
                sidebar.style.height = (content.offsetHeight) + 'px';
            } else {
                sidebar.style.height = (content.offsetHeight) + 'px';
                const contentMargin = parseInt(computedStyles.marginBottom);
                sidebar.style.height = (content.offsetHeight + contentMargin) + 'px';
            }
        }, 100);
    }
});

// Messages offset script
document.addEventListener('DOMContentLoaded', function() {
    const navbarHeight = document.querySelector('.navbar').offsetHeight;
    document.getElementById('messages-section').style.marginTop = (navbarHeight + 6) + 'px';
});

// Initialize all tooltips on the page
document.addEventListener('DOMContentLoaded', function () {
	const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
	const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
		return new bootstrap.Tooltip(tooltipTriggerEl);
	});
});