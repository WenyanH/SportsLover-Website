function createGroup() {
     window.open ("/create_group/", "Create Group", "height=550, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
}

function checkGroup(id) {
     window.open ("/group_detail/"+id, "Group Information", "height=550, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
}

function updateGroupInfo(id){
    window.open ("/update-group-info/"+id, "Group Information", "height=550, width=1000, top=0, left=0, toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
}

function showSearch() {
    var search = document.getElementById("hidesearch");
    if (search.style.display == "none") {
        search.style.display = "block";
    }
    else {
        search.style.display = "none";
    }
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
                        +"<div id=\"accept\"><a href=\"/delete-notification-accept-profile/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">Accept</button></a>"
                        +"<a href=\"/delete-notification-decline-profile/"+data[i]['id']+"\">"
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
                        +"<div id=\"accept\"><a href=\"/delete-notification-decline-profile/"+data[i]['id']+"\">"
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
                        +"<div id=\"accept\"><a href=\"/delete-news-accept-profile/"+data[i]['id']+"\">"
                        +"<button class=\"btn-primary\">Accept</button></a>"
                        +"<a href=\"/delete-news-decline-profile/"+data[i]['id']+"\">"
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
                        +"<div id=\"accept\"><a href=\"/delete-news-decline-profile/"+data[i]['id']+"\">"
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

$(document).ready(function () {
    var csrftoken = getCookie('csrftoken');
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });
    window.setInterval(updateNotifications, 3000);
});