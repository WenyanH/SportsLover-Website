function createGroup() {
     var check_login = document.getElementById("check_login");
     if (check_login.value=="AnonymousUser") {
        window.location.href="/login/?next=/group/"
     }else{
        subWin=window.open ("/create_group/", "Create Group", "height=600, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
        if(subWin.opener==null){
            subWin.opener=self;
        }
     }
}

function checkGroup(id) {
     subWin_2=window.open ("/group_detail/"+id, "Group Information", "height=600, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
     if(subWin_2.opener==null){
            subWin_2.opener=self;
        }
}

window.onload = function () {
    var check_login = document.getElementById("check_login");
    var login = document.getElementById("login");
    var user = document.getElementById("user");
    var notification = document.getElementById("notification");
    var settings = document.getElementById("settings")
    if (check_login.value!="AnonymousUser") {
        login.style.display = "none";
        user.style.display = "block";
        notification.style.display = "block";
        settings.style.display = "block";
    } else {
        login.style.display = "block";
        user.style.display = "none";
        notification.style.display = "none";
        settings.style.display = "none";
    }
}

$( document ).ready(function () {
    $("[name=classes]").click(showSubList);
    $("[name=classes]").next("ol").hide()
    $("[name=items]").click(itemFilter);
});

function showSubList() {
    var thisid = $(this).next("ol").attr("id");
    var d = document.getElementById(thisid);
    if (d.style.display == "none") {
        d.style.display = "block";
        var sportsclass = document.getElementById("classsport");
        sportsclass.value=thisid;
    }
    else {
        d.style.display = "none";
        var sportsclass = document.getElementById("classsport");
        sportsclass.value=thisid;
    }
}

function itemFilter() {
    var sportsitem = document.getElementById("itemsport");
    sportsitem.value=$(this).attr("id")
    searchform.submit()
}

function selectMorning() {
    var names = document.getElementsByName("time");
    for(var i=0; i<names.length; i++) {
        time = names[i].innerHTML;
        time = time.split(" ");
        hour = time[1].split(":")[0];
        hour = parseInt(hour);
        if (hour>=6 && hour<12){
            names[i].parentElement.style.display="table-row";
        }else{
            names[i].parentElement.style.display="none";
        }
    }
}

function selectAfternoon() {
    var names = document.getElementsByName("time");
    for(var i=0; i<names.length; i++) {
        time = names[i].innerHTML;
        time = time.split(" ");
        hour = time[1].split(":")[0];
        hour = parseInt(hour);
        if (hour>=12 && hour<18){
            names[i].parentElement.style.display="table-row";
        }else{
            names[i].parentElement.style.display="none";
        }
    }
}

function selectEvening() {
    var names = document.getElementsByName("time");
    for(var i=0; i<names.length; i++) {
        time = names[i].innerHTML;
        time = time.split(" ");
        hour = time[1].split(":")[0];
        hour = parseInt(hour);
        if (hour>=18 || hour<6){
            names[i].parentElement.style.display="table-row";
        }else{
            names[i].parentElement.style.display="none";
        }
    }
}

function selectBelowThree() {
    var sizes = document.getElementsByName("size");
    for(var i=0; i<sizes.length;i++) {
        size = sizes[i].innerHTML.split("&")[0];
        if(size<=3){
            sizes[i].parentElement.style.display="table-row";
        }else{
            sizes[i].parentElement.style.display="none";
        }
    }
}

function selectThreeToFive() {
    var sizes = document.getElementsByName("size");
    for(var i=0; i<sizes.length;i++) {
        size = sizes[i].innerHTML.split("&")[0];
        if(size<=5 && size>=3){
            sizes[i].parentElement.style.display="table-row";
        }else{
            sizes[i].parentElement.style.display="none";
        }
    }
}

function selectFiveToTen() {
    var sizes = document.getElementsByName("size");
    for(var i=0; i<sizes.length;i++) {
        size = sizes[i].innerHTML.split("&")[0];
        if(size<=10 && size>=5){
            sizes[i].parentElement.style.display="table-row";
        }else{
            sizes[i].parentElement.style.display="none";
        }
    }
}
function selectTenToTwenty() {
    var sizes = document.getElementsByName("size");
    for(var i=0; i<sizes.length;i++) {
        size = sizes[i].innerHTML.split("&")[0];
        if(size<=20 && size>=10){
            sizes[i].parentElement.style.display="table-row";
        }else{
            sizes[i].parentElement.style.display="none";
        }
    }
}

function selectAboveTwenty(){
    var sizes = document.getElementsByName("size");
    for(var i=0; i<sizes.length;i++) {
        size = sizes[i].innerHTML.split("&")[0];
        if(size>=20){
            sizes[i].parentElement.style.display="table-row";
        }else{
            sizes[i].parentElement.style.display="none";
        }
    }
}

function searchItem(){
    var searchitem = document.getElementById("hidesearch");
    sportsitem = searchitem.value;
    $.post("/search-item/", {"sportsitem":sportsitem})
    .done(function(data) {});
}
function updateNotifications() {
    var check_login = document.getElementById("check_login");
    if (check_login.value != "AnonymousUser") {
    $.post("/update-news/",{})
    .done(function(data) {
        if (data.length > 0){
            $("#new1").show();
            $("#new2").show();
            var list = $("#notification");
            var dropdown = $("<ul></ul>").attr("class","dropdown-menu");
        }
        for(var i=0; i<data.length; i++){
            if(data[i]['class']=='group'){
                if(data[i]['type']=="request"){
                    var li = $("<li></li>");
                    var link = $("<a></a>").attr("class", "hand").html(
                        "<i class=\"material-icons\">textsms</i>&nbsp"
                        +data[i]['context']
                        +"&nbsp&nbsp&nbsp"
                        +"<div id=\"accept\"><a href=\"/delete-notification-accept-group/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">Accept</button></a>"
                        +"<a href=\"/delete-notification-decline-group/"+data[i]['id']+"\">"
                        +"&nbsp&nbsp<button class=\"btn-warning\">Decline</button>"
                        +"</a></div>"
                    )
                    li.append(link);
                    dropdown.append(li);
                    list.append(dropdown);
                }
                if(data[i]['type']=="response"){
                    var li = $("<li></li>");
                    var link = $("<a></a>").attr("class", "hand").html(
                        "<i class=\"material-icons\">textsms</i>&nbsp"
                        +data[i]['context']
                        +"&nbsp&nbsp&nbsp"
                        +"<div id=\"accept\"><a href=\"/delete-notification-decline-group/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">OK</button></a></div>"
                    )
                    li.append(link);
                    dropdown.append(li);
                    list.append(dropdown);
                }
            }
            if(data[i]['class']=='friend'){
               if(data[i]['type']=="request"){
                    var li = $("<li></li>");
                    var link = $("<a></a>").attr("class", "hand").html(
                        "<i class=\"material-icons\">textsms</i>&nbsp"
                        +data[i]['context']
                        +"&nbsp&nbsp&nbsp"
                        +"<div id=\"accept\"><a href=\"/delete-news-accept-group/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">Accept</button></a>"
                        +"<a href=\"/delete-news-decline-group/"+data[i]['id']+"\">"
                        +"&nbsp&nbsp<button class=\"btn-warning\">Decline</button>"
                        +"</a></div>"
                    )
                    li.append(link);
                    dropdown.append(li);
                    list.append(dropdown);
                }
                if(data[i]['type']=="response"){
                    var li = $("<li></li>");
                    var link = $("<a></a>").attr("class", "hand").html(
                        "<i class=\"material-icons\">textsms</i>&nbsp"
                        +data[i]['context']
                        +"&nbsp&nbsp&nbsp"
                        +"<div id=\"accept\"><a href=\"/delete-news-decline-group/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">OK</button></a></div>"
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

function updateGroup() {
    var latest_time = $("p")[0].innerHTML;
    $.post("/update-groups/", {latest_time:latest_time})
    .done(function(data) {
        var tbody = $("#tbody");
        for(var i=0; i<data.groups.length; i++) {
            var content = $("<tr></tr>").html("<td><a href=\"javascript:checkGroup("
                +data.groups[i]['id']
                +")\"><p><b>"
                +data.groups[i]['subject']
                +"</b></p><a href=\"#\"><span class=\"post-info\">by "+data.groups[i]['owner']+"</span></a>"
                +"<span class=\"post-info\">&nbsp >> "+data.groups[i]['time']+"</span></td><td>"
                +data.groups[i]['sportsitem']+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</td><td>"
                +data.groups[i]['place']+"</td><td name=\"size\">"
                +data.groups[i]['size']+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</td><td name=\"time\">"
                +data.groups[i]['date_begin']+"</td><td>"
                +data.groups[i]['cost']+"$&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</td></tr>"
            )
            tbody.append(content);
        }
        $("p")[0].innerHTML = data.latest_time;
    });
}

function getCookie(name) {  
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

$(document).ready(function () {
    var csrftoken = getCookie('csrftoken');
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });
    window.setInterval(updateNotifications, 3000);
    window.setInterval(updateGroup, 5000);
});