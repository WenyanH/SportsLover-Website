$( document ).ready(function () {
    $("[name=classes]").click(showSubList);
    $("[name=classes]").next("ol").hide()
    $("[name=items]").click(itemFilter);
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
        searchform.submit()
    }
}

function itemFilter() {
    var sportsitem = document.getElementById("itemsport");
    sportsitem.value=$(this).attr("id")
    searchform.submit()
}