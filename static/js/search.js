
const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const tagsFilter = document.getElementById('tags-filter')
const resultsBox = document.getElementById('results-box')
const infiniteTrigger = document.getElementById('infinite-trigger')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

let infiniteViewpoint
let series = []
let scriptFlag = false

const sendSearchData = (searchTerm, selectedTags) => {

    // Change the URL to reflect the search term
    let newUrl = `/anime/`
    if (searchTerm.length > 0) {
        newUrl += `?search=${searchTerm.toLowerCase().replaceAll(' ', '-')}`
    }

    // Add tags to the URL
    if (selectedTags.length > 0 && searchTerm.length > 0) {
        newUrl += '&tags='
        for (let tag of selectedTags) {
            newUrl += tag.toLowerCase() + '+'
        }
        newUrl = newUrl.slice(0, -1)
    }
    if (selectedTags.length > 0 && searchTerm.length === 0) {
        newUrl += `?tags=`
        for (let tag of selectedTags) {
            newUrl += tag.toLowerCase() + '+'
        }
        newUrl = newUrl.slice(0, -1)
    }

    window.history.replaceState({}, '', newUrl)

    $.ajax({
         type: 'POST',
         url: 'search/',
         data: {
              'search_text': searchTerm,
              'tags[]': selectedTags,
              'csrfmiddlewaretoken': csrf
         },
         success: (response) => {
             // Reset the results box
             resultsBox.innerHTML = ''
             const data = response.data
             // data.sort((a, b) => (a.name_english > b.name_english ? 1 : -1));

             // Render the series
             if (Array.isArray(data)) {
                 renderSeries(data.slice(0, 10))
                 series = data.slice(10)

                 // Activate the infinite scroll after initial render
                 infiniteViewpoint = new Waypoint.Infinite({
                    element: $('.infinite-container')[0],
                    offset: 'bottom-in-view',
                    onBeforePageLoad: function () {
                        infiniteTrigger.click()
                    }
                })
             }
             // If no series match the search term, display a message
             else if (searchInput.value.length > 0) {
                 resultsBox.innerHTML = `<b>${data}</b>`
             }
             else {
                 resultsBox.innerHTML = ''
             }

         },
         error: (error) => {
              console.log(error)
         }
    })
}

const getSelectedTags = () => {
    const listItems = $("#tags-filter li");
    let selectedTags = [];
    listItems.each(function(idx, li) {
        // Query through all the tags and get the selected ones
        const checkbox = $(li).find(":checkbox");
        const label = $(li).find("label");
        if (checkbox.prop("checked")) {
            selectedTags.push(label.text());
        }
    })
    return selectedTags
}

const selectTags = (tags) => {
    const listItems = $("#tags-filter li");
    listItems.each(function(idx, li) {
        const checkbox = $(li).find(":checkbox");
        const label = $(li).find("label");
        if (tags.includes(label.text())) {
            checkbox.prop("checked", true);
        }
    })

}

const insertSearchQuery = (searchTerm) => {
    searchInput.value = searchTerm
}

const renderSeries = (data) => {
    data.forEach(series => {
         const animeUrl = `/anime/${series.web_name}/`; // Construct the URL
         resultsBox.innerHTML += `
        <a href="${animeUrl}" class="infinite-item">
        <div class="card list-card overflow-hidden">
            <div class="row g-0">
                <div class="col-sm-2">
                    <img src="${series.cover_image}" alt="...">
                </div>
                <div class="col-sm-10">
                    <div class="card-body">
                        <h5 class="card-title mb-1">${series.name_english}</h5>
                        <div class="card-text mb-2">${series.name_romaji}</div>
                        <div class="d-flex flex-row">
                            ${series.tags.map(tag => `<button class="btn btn-secondary me-1 tag">${tag}</button>`).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </a>
    `
     })
}

// Initial load before page load
addEventListener("DOMContentLoaded", (event) => {
    let searchTerm = JSON.parse(document.getElementById('search-term').textContent);
    let selectedTags = JSON.parse(document.getElementById('search-tags').textContent);
    if (searchTerm == null) {
        searchTerm = ''
    }
    if (selectedTags == null) {
        selectedTags = []
    }

    // Without the flag search runs twice
    scriptFlag = true
    insertSearchQuery(searchTerm)
    selectTags(selectedTags)
    scriptFlag = false

    sendSearchData(searchTerm, selectedTags)
})

// Event listener for tags filter
tagsFilter.onchange = e => {
    if (scriptFlag) return
    sendSearchData(searchInput.value, getSelectedTags())
}

// Event listener for search input
searchInput.oninput = e => {
    if (scriptFlag) return
    sendSearchData(e.target.value, getSelectedTags())
}

infiniteTrigger.onclick = e => {
    renderSeries(series.slice(0, 5))
    series = series.slice(5)
}
