const url = window.location.href;
const searchInput = document.getElementById('search-input');
const tagsFilter = document.getElementById('tags-filter');
const resultsBox = document.getElementById('results-box');
const infiniteTrigger = document.getElementById('infinite-trigger');
const sidebar = document.querySelector('.content-section > section');
const content = document.querySelector('.content-wrapper');
const csrf = getCookie('csrftoken');

let infiniteViewpoint;
let series = [];
let scriptFlag = false;

const sendSearchData = (searchTerm, selectedTags) => {
    let newUrl = `/anime/`;
    if (searchTerm.length > 0) {
        newUrl += `?search=${searchTerm.toLowerCase().replaceAll(' ', '-')}`;
    }

    if (selectedTags.length > 0 && searchTerm.length > 0) {
        newUrl += '&tags=';
        for (let tag of selectedTags) {
            newUrl += tag.toLowerCase() + '+';
        }
        newUrl = newUrl.slice(0, -1);
    }
    if (selectedTags.length > 0 && searchTerm.length === 0) {
        newUrl += `?tags=`;
        for (let tag of selectedTags) {
            newUrl += tag.toLowerCase() + '+';
        }
        newUrl = newUrl.slice(0, -1);
    }

    window.history.replaceState({}, '', newUrl);

    $.ajax({
        type: 'POST',
        url: 'search/',
        data: {
            'search_text': searchTerm,
            'tags[]': selectedTags,
            'csrfmiddlewaretoken': csrf
        },
        success: (response) => {
            resultsBox.innerHTML = '';
            const data = response;

            if (Array.isArray(data)) {
                console.log(response);
                renderSeries(data.slice(0, 10));
                series = data.slice(10);

                if (series.length > 0) {
                    infiniteViewpoint = new Waypoint.Infinite({
                        element: $('.infinite-container')[0],
                        offset: 'bottom-in-view',
                        onBeforePageLoad: function () {
                            infiniteTrigger.click();
                        }
                    });
                } else {
                    if (infiniteViewpoint) {
                        infiniteViewpoint.destroy();
                    }
                }
            } else if (searchInput.value.length > 0) {
                resultsBox.innerHTML = `<b>${data}</b>`;
            } else {
                resultsBox.innerHTML = '';
            }
        },
        error: (error) => {
            console.error('Error fetching search results:', error);
        }
    });
};

const getSelectedTags = () => {
    const listItems = $("#tags-filter li");
    let selectedTags = [];
    listItems.each(function (idx, li) {
        const checkbox = $(li).find(":checkbox");
        const label = $(li).find("label");
        if (checkbox.prop("checked")) {
            selectedTags.push(label.text());
        }
    });
    return selectedTags;
};

const selectTags = (tags) => {
    const listItems = $("#tags-filter li");
    listItems.each(function (idx, li) {
        const checkbox = $(li).find(":checkbox");
        const label = $(li).find("label");
        if (tags.includes(label.text())) {
            checkbox.prop("checked", true);
        }
    });
};

const insertSearchQuery = (searchTerm) => {
    searchInput.value = searchTerm;
};

const renderSeries = (data) => {
    let seriesHtml = '';
    data.forEach(series => {
        const animeUrl = `/anime/${series.web_name}/`;
        let englishTitles = getCookie('englishTitles') === 'true';
        let primaryTitle = englishTitles ? series.name_english : series.name_romaji;
        let secondaryTitle = englishTitles ? series.name_romaji : series.name_english;
        let seriesCard = `
        <a href="${animeUrl}" class="infinite-item">
            <div class="card list-card overflow-hidden">
                <div class="row g-0">
                    <div class="col-sm-2">
                        <img class="w-sm-100 h-sm-100 object-fit-cover" src="${series.image}" alt="Series Cover">
                    </div>
                    <div class="col-sm-10 ps-4 card-body flex-row d-flex align-items-center justify-content-between">
                        <div class="d-flex flex-column pb-1">
                            <h5 class="d-none d-md-block card-title mb-1">${primaryTitle.replace(/\\\"/g, '"')}</h5>
                            <h6 class="d-block d-md-none card-title mb-1">${primaryTitle.replace(/\\\"/g, '"')}</h6>
                            <div class="card-text mb-2">${secondaryTitle.replace(/\\\"/g, '"')}</div>
                            <div class="d-flex flex-row flex-wrap row-gap-1">
                                ${series.tags.map(tag => `<button class="btn btn-secondary me-2 mb-1 tag h-25">${tag}</button>`).join('')}
                            </div>
                        </div>
                        <div class="d-none d-md-block text-bg-success fs-5 me-3 px-2 py-1 rounded-3">${series.rating}</div>
                    </div>
                </div>
            </div>
        </a>
        `;
        if (series.rating > 65) {
            seriesCard = seriesCard.replace('text-bg-success', 'text-bg-success');
        } else if (series.rating > 50) {
            seriesCard = seriesCard.replace('text-bg-success', 'text-bg-warning');
        } else {
            seriesCard = seriesCard.replace('text-bg-success', 'text-bg-danger');
        }
        seriesHtml += seriesCard;
    });
    resultsBox.innerHTML += seriesHtml;
    sidebar.style.height = content.clientHeight + 'px';
};

addEventListener("DOMContentLoaded", (event) => {
    let searchTerm = JSON.parse(document.getElementById('search-term').textContent);
    let selectedTags = JSON.parse(document.getElementById('search-tags').textContent);
    if (searchTerm == null) {
        searchTerm = '';
    }
    if (selectedTags == null) {
        selectedTags = [];
    }

    scriptFlag = true;
    insertSearchQuery(searchTerm);
    selectTags(selectedTags);
    scriptFlag = false;

    sendSearchData(searchTerm, selectedTags);
});

tagsFilter.onchange = e => {
    if (scriptFlag) return;
    sendSearchData(searchInput.value, getSelectedTags());
};

searchInput.oninput = e => {
    if (scriptFlag) return;
    sendSearchData(e.target.value, getSelectedTags());
};

infiniteTrigger.onclick = e => {
    renderSeries(series.slice(0, 5));
    series = series.slice(5);
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}