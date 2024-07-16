
$(document).ready(function() {
    const url = window.location.href
    const tags = document.getElementsByClassName('tag-btn')

// Make every tag redirect to home page
    for (let tag of tags) {
        let tagLabel = tag.innerHTML
        tag.onclick = () => {
            window.location.href = `/anime/?tags=${tagLabel.toLowerCase()}`
        }
    }
})