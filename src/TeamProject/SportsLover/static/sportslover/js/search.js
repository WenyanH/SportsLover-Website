var geocoder;
var map, popup;
var places;
window.onload = function () {
    var check_login = document.getElementById("check_login");
    var login = document.getElementById("login");
    var signup = document.getElementById("signup");
    var user = document.getElementById("user");
    var notification = document.getElementById("notification");
    var settings = document.getElementById("settings")
    if (check_login.value != "AnonymousUser") {
        login.style.display = "none";
        signup.style.display = "none";
        user.style.display = "block";
        notification.style.display = "block";
        settings.style.display = "block";
    } else {
        login.style.display = "block";
        signup.style.display = "block";
        user.style.display = "none";
        notification.style.display = "none";
        settings.style.display = "none";
    }

    initialize();
    getJoinedGroup();
}

function giveItem() {
    var item = document.getElementById("sportsitem");
    item.value = "";
}

function checkItem() {
    var item = document.getElementById("sportsitem");
    if (item.value == "") {
        item.value = "Sports Item";
    }
}

function selectFree() {
    var item = document.getElementById("0");
    var expense = document.getElementById("expense");
    expense.value = item.text;
}

function selectTen() {
    var item = document.getElementById("1");
    var expense = document.getElementById("expense");
    expense.value = item.text;
}

function selectTwenty() {
    var item = document.getElementById("2");
    var expense = document.getElementById("expense");
    expense.value = item.text;
}

function selectFifty() {
    var item = document.getElementById("3");
    var expense = document.getElementById("expense");
    expense.value = item.text;
}

function selectHundred() {
    var item = document.getElementById("4");
    var expense = document.getElementById("expense");
    expense.value = item.text;
}

function selectMore() {
    var item = document.getElementById("5");
    var expense = document.getElementById("expense");
    expense.value = item.text;
}

function submitForm() {
    var sportsitem = document.getElementById("sportsitem")
    var date_begin = document.getElementById("date_begin");
    var date_end = document.getElementById("date_end");
    var expense = document.getElementById("expense");
    var item = document.getElementById("item");
    var start = document.getElementById("start");
    var end = document.getElementById("end");
    var money = document.getElementById("money");
    item.value = sportsitem.value;
    start.value = date_begin.value;
    end.value = date_end.value;
    money.value = expense.value;
    searchform = document.getElementById("searchform");
    if (item.value == "Sports Item") {
        item.value = "";
    }
    if (money.value == "Expense") {
        money.value = "";
    }
    if (start.value == "Start Date") {
        start.value = "";
    }
    if (end.value == "End Date") {
        end.value = "";
    }
    searchform.submit()
}

function updateNotifications() {
    var check_login = document.getElementById("check_login");
    if (check_login.value != "AnonymousUser") {
    $.post("/update-news/", {})
        .done(function (data) {
            if (data.length > 0) {
                $("#new1").show();
                $("#new2").show();
                var list = $("#notification");
                var dropdown = $("<ul></ul>").attr("class", "dropdown-menu");
            }
            for (var i = 0; i < data.length; i++) {
                if (data[i]['class'] == 'group') {
                    if (data[i]['type'] == "request") {
                        var li = $("<li></li>");
                        var link = $("<a></a>").attr("class", "hand").html(
                            "<i class=\"material-icons\">textsms</i>&nbsp"
                            + data[i]['context']
                            + "&nbsp&nbsp&nbsp"
                            + "<div id=\"accept\"><a href=\"/delete-notification-accept-search/" + data[i]['id'] + "\">"
                            + "<button class=\"btn-primary\">Accept</button></a>"
                            + "<a href=\"/delete-notification-decline-search/" + data[i]['id'] + "\">"
                            + "&nbsp&nbsp<button class=\"btn-warning\">Decline</button>"
                            + "</a></div>"
                        )
                        li.append(link);
                        dropdown.append(li);
                        list.append(dropdown);
                    }
                    if (data[i]['type'] == "response") {
                        var li = $("<li></li>");
                        var link = $("<a></a>").attr("class", "hand").html(
                            "<i class=\"material-icons\">textsms</i>&nbsp"
                            + data[i]['context']
                            + "&nbsp&nbsp&nbsp"
                            + "<div id=\"accept\"><a href=\"/delete-notification-decline-search/" + data[i]['id'] + "\">"
                            + "<button class=\"btn-primary\">OK</button></a></div>"
                        )
                        li.append(link);
                        dropdown.append(li);
                        list.append(dropdown);
                    }
                }
                if (data[i]['class'] == 'friend') {
                    if (data[i]['type'] == "request") {
                        var li = $("<li></li>");
                        var link = $("<a></a>").attr("class", "hand").html(
                            "<i class=\"material-icons\">textsms</i>&nbsp"
                            + data[i]['context']
                            + "&nbsp&nbsp&nbsp"
                            + "<div id=\"accept\"><a href=\"/delete-news-accept-search/" + data[i]['id'] + "\">"
                            + "<button class=\"btn-primary\">Accept</button></a>"
                            + "<a href=\"/delete-news-decline-search/" + data[i]['id'] + "\">"
                            + "&nbsp&nbsp<button class=\"btn-warning\">Decline</button>"
                            + "</a></div>"
                        )
                        li.append(link);
                        dropdown.append(li);
                        list.append(dropdown);
                    }
                    if (data[i]['type'] == "response") {
                        var li = $("<li></li>");
                        var link = $("<a></a>").attr("class", "hand").html(
                            "<i class=\"material-icons\">textsms</i>&nbsp"
                            + data[i]['context']
                            + "&nbsp&nbsp&nbsp"
                            + "<div id=\"accept\"><a href=\"/delete-news-decline-search/" + data[i]['id'] + "\">"
                            + "<button class=\"btn-primary\">OK</button></a></div>"
                        )
                        li.append(link);
                        dropdown.append(li);
                        list.append(dropdown);
                    }
                }
                if(data[i]['class']=='comment'){
                    var li = $("<li></li>");
                    var link = $("<a></a>").attr("class", "hand").html(
                        "<i class=\"material-icons\">textsms</i>&nbsp"
                        +data[i]['context']
                        +"&nbsp&nbsp&nbsp"
                        +"<div id=\"accept\"><a href=\"/add-comment/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">OK</button></a>"
                        +"</div>"
                    )
                    li.append(link);
                    dropdown.append(li);
                    list.append(dropdown);
                }
                if(data[i]['class']=='delete'){
                    var li = $("<li></li>");
                    var link = $("<a></a>").attr("class", "hand").html(
                        "<i class=\"material-icons\">textsms</i>&nbsp"
                        +data[i]['context']
                        +"&nbsp&nbsp&nbsp"
                        +"<div id=\"accept\"><a href=\"/delete-confirm/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">OK</button></a>"
                        +"</div>"
                    )
                    li.append(link);
                    dropdown.append(li);
                    list.append(dropdown);
                }
            }
        });
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function initialize() {
    geocoder = new google.maps.Geocoder();
    popup = new google.maps.InfoWindow();
    var latlng = new google.maps.LatLng(40.4434699, -79.9456454);		// map center: CMU
    var mapOptions = {
        zoom: 10,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function () {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function (marker) {
            marker.setMap(null);
        });
        markers = [];

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function (place) {
            var icon = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
                map: map,
                icon: icon,
                title: place.name,
                position: place.geometry.location
            }));

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });

}

function getJoinedGroup() {
    $.get("/get-places/").done(function (data) {
        places = data['address'];
        costs = data['cost'];
        sizes = data['size'];
        subjects = data['subject'];
        date_begins =  data['date_begin'];
        date_ends = data['date_end'];
        ids = data['id']
        owners = data['owner'];
        showPlaces(places, costs, sizes, subjects, date_begins, date_ends, owners, ids);
    });
}

function checkGroup(id) {
    subWin_2=window.open ("/group_detail/"+id, "Group Information", "height=600, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
    if(subWin_2.opener==null){
        subWin_2.opener=self;
    }
}

function codeAddress(address, cost, size, subject, date_begin, date_end, owner, id) {
    geocoder.geocode({'address': address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            //map.setCenter(results[0].geometry.location);

            // InfoWindow content
            var content = '<div id="iw-container">' +
                '<div class="iw-title"><a href="javascript:checkGroup('+ id +')">' + subject + '</a></div>' +
                '<div class="iw-content">' +
                '<div class="iw-subTitle">Group Information</div>' +
                '<p> group size: ' + size + '</p>' +
                '<p> group cost: ' + cost + '</p>' +
                '<p> group address: ' + address + '</p>' +
                '<p> group owner: ' + owner + '</p>' +
                '<p> begin time: ' + date_begin + '</p>' +
                '<p> end time: ' + date_end + '</p>' +
                '<div class="iw-bottom-gradient"></div>' +
                '</div>';

            var marker = new google.maps.Marker({
                map: map, position: results[0].geometry.location
            });

            var infowindow = new google.maps.InfoWindow({
                content: content,
                maxWidth: 350
            });

            google.maps.event.addListener(marker, 'click', function () {
                infowindow.open(map, marker);
            });

            // Event that closes the Info Window with a click on the map
            google.maps.event.addListener(map, 'click', function () {
                infowindow.close();
            });
        }
    });
}

function showPlaces(places, costs, sizes, subjects, date_begins, date_ends, owners, ids) {
    for (var i = 0; i < places.length; i++) {
        codeAddress(places[i], costs[i], sizes[i], subjects[i], date_begins[i], date_ends[i], owners[i], ids[i]);
    }
}

$(document).ready(function () {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    window.setInterval(updateNotifications, 3000);
});
