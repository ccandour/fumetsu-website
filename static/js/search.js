
const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const tagsFilter = document.getElementById('tags-filter')
const resultsBox = document.getElementById('results-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (searchTerm, selectedTags) => {
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

             // Render the series
             if (Array.isArray(data)) {
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
                                        ${series.tags.map(tag => `<button class="btn btn-secondary me-1">${tag}</button>`).join('')}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    </a>
                `

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

let getSelectedTags = () => {
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

tagsFilter.onchange = e => {
    sendSearchData(searchInput.value, getSelectedTags())
}

// Event listener for search input
searchInput.oninput = e => {
    sendSearchData(e.target.value, getSelectedTags())
}

// Initial load
document.addEventListener("DOMContentLoaded", () => {
    sendSearchData('', '')
})