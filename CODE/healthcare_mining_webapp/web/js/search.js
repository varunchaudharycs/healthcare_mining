$(document).ready(function () {

    $("#related_symptoms").css('visibility', 'hidden');

    $('#search_selection').change(function () {
        $('div.response').css('display', 'none');
        $('div.posts').css('display', 'none');
        $('div.posts_title').css('display', 'none');
        $('div.disease_title').css('display', 'none');
        $('div.drug_title').css('display', 'none');
        $('div.drug').css('display', 'none');

        $("#related_symptoms").css('visibility', 'hidden');
    })

    // add event listener for Enter button to invoke search
    var input = document.getElementById("search_box");
    input.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            event.preventDefault();
            // Trigger the button element with a click
            document.getElementById("search_button").click();
        }
    });

})

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
    // response json parsed from response
    const res = JSON.parse(response);

    if (res != '') {

        if(res.hasOwnProperty('related_symptoms') && res.related_symptoms.length > 0) {
            var newLabel = '<b>Related Symptoms: </b>';
            for (var i = 0; i < res.related_symptoms.length; i++) {
                if (i != 0) {
                    newLabel += ', ';
                }
                newLabel += res.related_symptoms[i];
            }
            $("#related_symptoms").html(newLabel);
            $("#related_symptoms").css('visibility', 'visible');
        }
        else {
            $("#related_symptoms").css('visibility', 'hidden');
        }


        if($('#search_selection').val() == 'disease_search') {
            $('div.response').css('display', 'inline-block');
            $('div.posts').css('display', 'inline-block');
            $('div.posts_title').css('display', 'inline-block');
            $('div.disease_title').css('display', 'inline-block');
            $('div.drug_title').css('display', 'none');
            $('div.drug').css('display', 'none');
            $('div.response').empty();
            $('div.posts').empty();
            $('div.drug').empty();

            if(res.results.hasOwnProperty('mayo_clinic')){
                    if (res.results.mayo_clinic.length > 0) {
                    var list = "";
                    var displaysize = 5;
                    if (res.results.mayo_clinic.length < displaysize) {
                        displaysize = res.results.mayo_clinic.length
                    }
                    for (var i = 0; i < displaysize; i++) {
                        var item = res.results.mayo_clinic[i];

                        var symptoms = "<b>Symptoms: </b>";
                        if(item.hasOwnProperty('other_symptoms')){
                            for (var j = 0; j < item.other_symptoms.length; j++) {
                                if (j != 0) {
                                    symptoms += ", "
                                }
                                const ss = item.other_symptoms[j];
                                var found = false;
                                for (var k = 0; k < res.tagged_symptoms.length; k++) {
                                    console.log(ss)
                                    console.log(res.tagged_symptoms[k])
                                    if (res.tagged_symptoms[k] === ss) {
                                        found = true;
                                        break;
                                    }
                                }
                                if (found) {
                                    symptoms += "<span style='background-color: #ffe230'>" + ss + "</span>"
                                }
                                else {
                                    symptoms += ss;
                                }
                            }
                        }

                        list += "<ul>";
                        list += "<li class='title_li'><a href='" + item.url + "' target='_blank'>" + item.title + "</a></li>";
                        list += "<ul>";
                        list += "<li class = 'description'>" + item.summary.substring(0, 200) + "...</li>";
                        list += "<li class = 'description'>" + symptoms + "</li>";
                        list += "</ul>";
                        list += "</ul>";
                        list += "<hr class='hr_line'>";
                    }
                    setTimeout(function () {
                        $(".response").append(list);
                    });
                }
            }

            var list_posts = "";
            if(res.results.hasOwnProperty('web_md_mb')) {
                if (res.results.web_md_mb.length > 0) {
                    var displaysize = 5;
                    if (res.results.web_md_mb.length < displaysize) {
                        displaysize = res.results.web_md_mb.length
                    }
                    for (var i = 0; i < displaysize; i++) {
                        var item = res.results.web_md_mb[i];

                        var symptoms = "<b>Symptoms: </b>";
                        if(item.hasOwnProperty('other_symptoms')){
                            for (var j = 0; j < item.other_symptoms.length; j++) {
                                if (j != 0) {
                                    symptoms += ", "
                                }
                                const ss = item.other_symptoms[j];
                                var found = false;
                                for (var k = 0; k < res.tagged_symptoms.length; k++) {
                                    console.log(ss)
                                    console.log(res.tagged_symptoms[k])
                                    if (res.tagged_symptoms[k] === ss) {
                                        found = true;
                                        break;
                                    }
                                }
                                if (found) {
                                    symptoms += "<span style='background-color: #ffe230'>" + ss + "</span>"
                                }
                                else {
                                    symptoms += ss;
                                }
                            }
                        }

                        list_posts += "<ul>";
                        list_posts += "<li class='title_li'><a href='" + item.url + "' target='_blank'>" + item.title + "</a></li>";
                        list_posts += "<ul>";
                        // list_posts += "<li class='description'>" + item.summary.substring(0, 200) + " (<a href = '" + item.url + "' " + "target='_blank'" + "color ='blue'" + " >" + item.url + "</a>) </li>";
                        list_posts += "<li class='description'>" + item.summary.substring(0, 200) + "...</li>";
                        list_posts += "<li class = 'description'>" + symptoms + "</li>";
                        list_posts += "</ul>";
                        list_posts += "</ul>";
                        list_posts += "<hr class='hr_line'>"
                    }
                }
            }

            if(res.results.hasOwnProperty('patient_info')) {
                if (res.results.patient_info.length > 0) {
                    var displaysize = 5;
                    if (res.results.patient_info.length < displaysize) {
                        displaysize = res.results.patient_info.length
                    }

                    for (var i = 0; i < displaysize; i++) {
                        var item = res.results.patient_info[i];
                        var symptoms = "<b>Symptoms: </b>";
                        if(item.hasOwnProperty('other_symptoms')){
                            for (var j = 0; j < item.other_symptoms.length; j++) {
                                if (j != 0) {
                                    symptoms += ", "
                                }
                                const ss = item.other_symptoms[j];
                                var found = false;
                                for (var k = 0; k < res.tagged_symptoms.length; k++) {
                                    console.log(ss)
                                    console.log(res.tagged_symptoms[k])
                                    if (res.tagged_symptoms[k] === ss) {
                                        found = true;
                                        break;
                                    }
                                }
                                if (found) {
                                    symptoms += "<span style='background-color: #ffe230'>" + ss + "</span>"
                                }
                                else {
                                    symptoms += ss;
                                }
                            }
                        }

                        list_posts += "<ul>";
                        list_posts += "<li class='title_li'><a href='" + item.url + "' target='_blank'>" + item.title + "</a></li>";
                        list_posts += "<ul>";
                        // list_posts += "<li class='description'>" + item.summary.substring(0, 100) + " (<a href = '" + item.url + "' " + "target='_blank'" + "color ='blue'" + " >" + item.url + "</a>) </li>";
                        list_posts += "<li class='description'>" + item.summary.substring(0, 200) + "...</li>";
                        list_posts += "<li class = 'description'>" + symptoms + "</li>";
                        list_posts += "</ul>";
                        list_posts += "</ul>";
                        list_posts += "<hr class='hr_line'>"
                    }
                }
            }

            setTimeout(function () {
                $(".posts").append(list_posts);
            });
        }
        else
        if($('#search_selection').val() == 'drug_search') {
            $('div.response').css('display', 'none');
            $('div.posts').css('display', 'none');
            $('div.drug').css('display', 'inline-block');
            $('div.posts_title').css('display', 'none');
            $('div.disease_title').css('display', 'none');
            $('div.drug_title').css('display', 'inline-block');
            $('div.drug').empty();

            var drug_list = "";
            if(res.results.length != 0){
                for (var i = 0; i < 5; i++) {
                    var item = res.results[i];
                    drug_list += "<ul>";
                    // drug_list += "<li class='title_li'>" + item.drug_name + "</li>";
                    drug_list += "<li class='title_li'><a href='" + item.drug_detail_page + "' target='_blank'>" + item.drug_name + "</a></li>";
                    drug_list += "<ul>";
                    // drug_list += "<li class='description'>" + " (<a href = '" + item.drug_review_page + "' " + "target='_blank'" + "color ='blue'" + " >" + item.drug_review_page + "</a>) </li>";
                    drug_list += "<li class='description'>" + " (<a href = '" + item.drug_review_page + "' " + "target='_blank'" + "color ='blue'" + " > Check user reviews" + "</a>) </li>";
                    drug_list += "</ul>";
                    drug_list += "</ul>";
                    drug_list += "<hr class='hr_line'>"
                }
                setTimeout(function () {
                    $(".drug").append(drug_list);
                });
            }
            else {
                $(".drug").append("<h4>No Matching Drugs Found.</h4>");
            }
        }
    } else {
        swal("Don't Worry! It doesn't seem like any disease as per the results!");
    }
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