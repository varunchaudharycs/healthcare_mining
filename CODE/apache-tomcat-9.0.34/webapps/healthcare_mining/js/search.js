function sendSearchRequest() {
    var searchQuery = $('#search_box').val();
    searchQuery = searchQuery.trim();
    const selectedSearchOption = document.getElementById("search_selection").value;
    // empty search is not allowed, show alert
    if (searchQuery === '') {
        if (selectedSearchOption === 'disease_search') {
            swal( "Empty Search Query" ,  "Please type the symptoms you want to search." ,  "error" );
        }
        else if (selectedSearchOption === 'drug_search') {
            swal("Empty Search Query", "Please type the disease name you want to search.", "error");
        }
    }

    ajaxGetRequest(window.location.href + '/search?query=' + searchQuery + '&type=' + selectedSearchOption, handleSearchResponse)
}

function handleSearchResponse(response) {
    console.log(response)
}

function searchOptionChange() {
    const selectedValue = document.getElementById("search_selection").value;
    if (selectedValue === 'drug_search') {
        //reset the value to avoid unwanted search
        document.getElementById('search_box').value = '';
        document.getElementById("search_box").placeholder = "Type the disease name here...";
    }
    else {
        //reset the value to avoid unwanted search
        document.getElementById('search_box').value = '';
        document.getElementById("search_box").placeholder = "Type the symptoms here...";
    }
}
