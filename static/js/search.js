
const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const tagsFilter = document.getElementById('tags-filter')
const resultsBox = document.getElementById('results-box')
const infiniteTrigger = document.getElementById('infinite-trigger')
const sidebar = document.querySelector('.content-section > section');
const content = document.querySelector('.content-wrapper');
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
         const animeUrl = `/anime/${series.web_name}/` // Construct the URL
         let seriesHtml = `
        <a href="${animeUrl}" class="infinite-item">
        <div class="card list-card overflow-hidden">
            <div class="row g-0">
                <div class="col-sm-2">
                    <img src="${series.image}" alt="Series Cover">
                </div>
         
                <div class="col-sm-10 ps-4 card-body flex-row d-flex align-items-center justify-content-between">
                    <div class="d-flex flex-column pb-1">
                        <h5 class="d-none d-md-block card-title mb-1">${series.name_english}</h5>
                        <h6 class="d-block d-md-none card-title mb-1">${series.name_english}</h6>
                        <div class="card-text mb-2">${series.name_romaji}</div>
                        <div class="d-flex flex-row flex-wrap row-gap-1">
                            ${series.tags.map(tag => `<button class="btn btn-secondary me-1 tag h-25">${tag}</button>`).join('')}
                        </div>
                    </div>
                    <div class=" d-none d-md-block text-bg-success fs-5 me-3 px-2 py-1 rounded-3">${series.rating}</div>
                </div>
                
                   
                </div>
         
            </div>
        </div>
        </a>
    `
        if (series.rating > 65) {
             seriesHtml = seriesHtml.replace('text-bg-success', 'text-bg-success')
        }
        else if (series.rating > 50) {
            seriesHtml = seriesHtml.replace('text-bg-success', 'text-bg-warning')
        }
        else {
            seriesHtml = seriesHtml.replace('text-bg-success', 'text-bg-danger')
        }
        resultsBox.innerHTML += seriesHtml

        // Resize the sidebar to match the content
        sidebar.style.height = content.clientHeight + 'px'

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
